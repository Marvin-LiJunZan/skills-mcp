# -*- coding: utf-8 -*-
"""推送文章到微信公众号草稿箱（只用 Python 标准库，无需 pip）。

用法:
  set WECHAT_APPID=xxx & set WECHAT_SECRET=xxx   (Windows cmd)
  export WECHAT_APPID=xxx WECHAT_SECRET=xxx      (bash)

  python publish_draft.py \
    --title "标题(<=21个汉字)" \
    --digest "摘要(<=54字)" \
    --html content.html \
    --cover cover.png \
    --img IMG1=path/图1.png --img IMG2=path/图2.png \
    [--author 未筑之境]

HTML 正文里的 {{IMG1}} 占位符会被替换为上传后的微信图片 URL。
常见错误: 40164=IP不在白名单(去后台加当前公网IP); 40001=Secret错; 48001=接口无权限。
"""
import argparse
import json
import os
import sys
import uuid
import urllib.request
import urllib.parse


def http_get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def http_post_json(url, payload):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def http_post_file(url, filepath):
    boundary = uuid.uuid4().hex
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        filedata = f.read()
    body = b"\r\n".join([
        ("--" + boundary).encode(),
        ('Content-Disposition: form-data; name="media"; filename="%s"' % filename).encode("utf-8"),
        b"Content-Type: image/png",
        b"",
        filedata,
        ("--" + boundary + "--").encode(),
        b"",
    ])
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "multipart/form-data; boundary=" + boundary})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def check(resp, step):
    if resp.get("errcode") not in (None, 0):
        sys.exit("步骤[%s]失败: %s" % (step, json.dumps(resp, ensure_ascii=False)))
    return resp


def load_env():
    """自动加载 .env 配置文件（优先保留已存在的系统环境变量）"""
    search_dirs = [
        os.getcwd(),
        os.path.dirname(os.path.abspath(__file__)),
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    ]
    for d in search_dirs:
        env_file = os.path.join(d, ".env")
        if os.path.isfile(env_file):
            try:
                with open(env_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
                break
            except Exception:
                pass


def main():
    load_env()
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--digest", required=True)
    p.add_argument("--html", required=True)
    p.add_argument("--cover", required=True)
    p.add_argument("--author", default=os.environ.get("WECHAT_AUTHOR", "未筑之境"))
    p.add_argument("--img", action="append", default=[],
                   help="占位符=图片路径，可多次传入，如 --img IMG1=a.png")
    args = p.parse_args()

    appid = os.environ.get("WECHAT_APPID", "")
    secret = os.environ.get("WECHAT_SECRET", "")
    if not appid or not secret:
        sys.exit("缺少环境变量 WECHAT_APPID / WECHAT_SECRET")

    q = urllib.parse.urlencode({"grant_type": "client_credential",
                                "appid": appid, "secret": secret})
    tok = check(http_get("https://api.weixin.qq.com/cgi-bin/token?" + q), "获取token")
    token = tok["access_token"]
    print("1. access_token 获取成功")

    with open(args.html, encoding="utf-8") as f:
        content = f.read()

    for spec in args.img:
        key, _, path = spec.partition("=")
        if not key or not path:
            sys.exit("--img 格式应为 占位符=路径，收到: " + spec)
        u = check(http_post_file(
            "https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=" + token, path),
            "上传正文图 " + key)
        content = content.replace("{{" + key + "}}", u["url"])
        print("   正文图 %s 上传成功" % key)

    cov = check(http_post_file(
        "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=" + token + "&type=image",
        args.cover), "上传封面")
    print("2. 封面上传成功, media_id=" + cov["media_id"])

    draft = {"articles": [{
        "title": args.title, "author": args.author, "digest": args.digest,
        "content": content, "thumb_media_id": cov["media_id"],
        "need_open_comment": 1, "only_fans_can_comment": 0,
    }]}
    res = check(http_post_json(
        "https://api.weixin.qq.com/cgi-bin/draft/add?access_token=" + token, draft), "创建草稿")
    print("3. 草稿创建成功, media_id=" + res["media_id"])
    print("完成! 前往 mp.weixin.qq.com -> 内容管理 -> 草稿箱 查看并手动发布")


if __name__ == "__main__":
    main()
