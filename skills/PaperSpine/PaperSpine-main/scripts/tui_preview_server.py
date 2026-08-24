#!/usr/bin/env python3
"""Serve a browser preview of the PaperSpine terminal UI."""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HTML = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PaperSpine TUI Preview</title>
<style>
:root {
  color-scheme: dark;
  --bg: #080808;
  --panel: #0e0e0e;
  --line: #d97952;
  --text: #f2f2f2;
  --muted: #777;
  --soft: #b9b9b9;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  min-height: 100vh;
  background: radial-gradient(circle at 50% 0%, #151515 0, var(--bg) 48%);
  color: var(--text);
  font: 18px/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, "Cascadia Mono", monospace;
  display: grid;
  place-items: center;
  padding: 28px;
}
.terminal {
  width: min(1280px, 96vw);
  min-height: 720px;
  border: 2px solid var(--line);
  border-radius: 8px;
  background: #050505;
  box-shadow: 0 24px 80px rgba(0,0,0,.55);
  overflow: hidden;
}
.top {
  height: 44px;
  border-bottom: 2px solid var(--line);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--line);
  font-weight: 700;
  letter-spacing: .04em;
}
.welcome {
  min-height: 676px;
  display: grid;
  place-items: center;
  text-align: center;
  padding: 42px;
}
.mountain {
  white-space: pre;
  color: white;
  font-weight: 700;
  line-height: 1.05;
  margin: 22px 0 16px;
}
.title {
  color: white;
  font-size: clamp(44px, 8vw, 96px);
  line-height: .9;
  font-weight: 900;
  letter-spacing: .04em;
  margin: 8px 0 24px;
}
.intro {
  max-width: 860px;
  margin: 0 auto;
  color: #e8e8e8;
}
.intro p { margin: 6px 0; }
.social {
  margin-top: 28px;
  color: var(--soft);
  display: grid;
  gap: 5px;
}
.config {
  display: grid;
  grid-template-columns: 30% 70%;
  min-height: 676px;
}
.left, .right {
  padding: 34px 28px;
}
.left {
  border-right: 2px solid var(--line);
  display: grid;
  align-content: center;
  gap: 9px;
  text-align: center;
}
.field {
  color: var(--muted);
}
.field.active {
  color: white;
  font-weight: 800;
}
.right {
  display: grid;
  align-content: center;
  gap: 28px;
}
.hint {
  color: var(--muted);
  text-align: center;
}
.options {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 3ch;
  align-items: center;
  text-align: center;
}
.option {
  color: var(--muted);
  min-height: 80px;
  display: grid;
  place-items: center;
  border: 1px solid #222;
  border-radius: 6px;
  padding: 16px;
}
.option.current {
  color: white;
  border-color: var(--line);
  box-shadow: inset 0 0 0 1px rgba(217,121,82,.35);
}
.current-value {
  text-align: center;
  color: white;
  font-size: 24px;
}
nav {
  position: fixed;
  right: 28px;
  bottom: 24px;
  display: flex;
  gap: 10px;
}
nav a {
  color: white;
  border: 1px solid var(--line);
  padding: 8px 12px;
  border-radius: 6px;
  text-decoration: none;
  background: rgba(0,0,0,.45);
}
</style>
</head>
<body>
<main class="terminal">
  <div class="top">PaperSpine TUI Preview</div>
  __BODY__
</main>
<nav><a href="/">启动页</a><a href="/config">配置页</a></nav>
</body>
</html>"""

WELCOME = r"""
<section class="welcome">
  <div>
    <div>Welcome back!</div>
    <div class="mountain">                 /\                         /\
        /\      /  \        /\      /\     /  \       /\
   /\  /  \    /    \  /\  /  \    /  \   /    \  /\  /  \
__/  \/    \__/      \/  \/    \__/    \_/      \/  \/    \__</div>
    <div class="title">PaperSpine</div>
    <div class="intro">
      <p>我们做 PaperSpine，是为了让 AI 先学习，再写作。</p>
      <p>不是把论文润色得更长，而是把动机、证据与结构连成一条清晰主线。</p>
      <p>它面向论文、报告与竞赛写作：调研目标场景，学习优秀样例，再逐段生成。</p>
    </div>
    <div class="social">
      <div>𝕏  X：Wbingo353332</div>
      <div>♪  抖音：91362158854</div>
      <div>▣  小红书：4770513150</div>
    </div>
  </div>
</section>"""

CONFIG = """
<section class="config">
  <aside class="left">
    <div class="field">01. 工作流</div>
    <div class="field">02. 目标场景</div>
    <div class="field active">03. 调研深度</div>
    <div class="field">04. 最终输出语言</div>
    <div class="field">05. Word 版本</div>
    <div class="field">06. 生成英文产物后是否翻译</div>
    <div class="field">07. 目标名称</div>
    <div class="field">08. 初稿路径</div>
    <div class="field">09. 素材文件夹路径</div>
    <div class="field">10. 初始动机假设</div>
    <div class="field">11. 官方链接</div>
    <div class="field">12. 特殊要求</div>
    <div class="field">13. 界面语言</div>
  </aside>
  <section class="right">
    <div class="hint">←/→ 切换选项；↑/↓ 切换字段；Enter 编辑/确认；S 保存；Q 退出</div>
    <div class="options">
      <div class="option">轻量调研：3+3 篇样例加官方要求</div>
      <div class="option current">深度调研：6+6 篇样例加官方要求</div>
      <div class="option">轻量调研：3+3 篇样例加官方要求</div>
    </div>
    <div class="current-value">当前字段：调研深度 = pro</div>
  </section>
</section>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        body = CONFIG if self.path.startswith("/config") else WELCOME
        payload = HTML.replace("__BODY__", body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"PaperSpine TUI preview: http://{args.host}:{args.port}")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
