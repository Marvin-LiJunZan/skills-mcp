---
name: wechat-oa-weizhu
description: 「未筑之境」微信公众号端到端运营工作流。触发词：未筑之境、研究生生存栈、公众号推文、写公众号、发公众号、推草稿箱、公众号配图、公众号排版。覆盖：写文章（文风硬规则）、起标题（8选1）、做配图（蓝金 HTML 模板 + Edge 无头渲染）、推送草稿箱（微信 API）、发布检查、冷启动运营。
agent_created: true
---

# 微信公众号运营 · 未筑之境

把一篇文章从选题做到草稿箱的完整工作流。任何一步都可以单独使用。

## 账号档案

- 账号：未筑之境（个人订阅号）
- 定位一句话：用 AI 工具栈帮研究生把科研效率拉满。
- 主干系列：研究生生存栈（编号 00、01、02……），6 层 Research Stack：超级搜索 → Git → VS Code → Cursor → Codex → Antigravity。
- 内容支柱配比：主干系列 60%｜科研踩坑与心法 30%｜互动动态 10%。
- 品牌色板（蓝金，严格固定）：
  - 主深蓝 `#0C2242`｜辅助深蓝 `#123058`｜品牌金 `#D4A93C`｜亮金 `#E8C56A`（仅图片内）
  - 正文灰黑 `#3A3F4B`｜注释灰 `#8A93A6`｜浅底纹 `#F4F7FB`

## 第 1 步：写文章

规则细节见 `references/style-rules.md`，硬红线先记住：

- 正文 1500 到 2500 字，每段 1 到 3 句，段间空一行。
- 禁止破折号；禁止「不是 X，而是 Y」类否定框架句式；数字用阿拉伯数字；中英文之间加空格。
- 结构：钩子开场（2 到 3 段）→ 图 → 小节 → 图 → 小节 → 系列预告 + 关注 CTA。任何位置连续文字不超过 3 屏，小节 4 到 7 个。
- 文末必须有 1 个引导留言的具体问题 + 1 句转发钩子。
- 写完后跑自检：违禁词 0｜否定框架 0｜破折号 0｜超 3 句段落 0。

## 第 2 步：起标题（8 选 1）

- 恰好 8 个候选，覆盖稳妥 / 平衡 / 传播三档力度，逐项打分，推荐 1 个最优 + 1 个更稳妥 + 1 个更强传播。
- 硬约束：不出现引号、冒号、破折号；两个以上分句用逗号连接；夸张必须与正文一致；64 字节（约 21 个汉字）以内。
- 系列偏好句式：「同样 X，为什么有人 A 有人 B」（00、01 篇均用此句式，保持系列辨识度）。
- 摘要手写，54 字以内，讲清读者收益，开头补「研究生生存栈 0X」。

## 第 3 步：做配图（蓝金 HTML 模板 + Edge 无头渲染）

模板在 `templates/`，共 4 种：封面 `cover.html`（900×383）、双栏对比 `compare.html`（1080×660）、步骤流程 `flow.html`（1080×620）、分层总览 `stack.html`（1080×820）。模板里的文字是示例，全文替换文字即可，版式和配色不要动。

渲染（Windows，Edge 无头截图，2 倍清晰度）：

```bash
bash scripts/render_images.sh 900x383 templates/cover.html 输出/cover.png
# 可一次传多组： render_images.sh 宽x高 输入.html 输出.png [宽x高 输入2.html 输出2.png ...]
```

脚本会自动找 Edge（`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`，其次 Chrome）。渲染后必须肉眼检查 PNG 效果再使用。

经验：带中文文字的示意图/封面不要用 AI 生图（文字会乱码），用 HTML 模板渲染，版式可控、风格统一、可复用。

## 第 4 步：推送草稿箱（微信 API）

正文排版：把 Markdown 转成**内联样式 HTML**（微信过滤 `<style>` 标签），正文图片占位符写成 `{{IMG1}}`、`{{IMG2}}`。参照 `references/style-rules.md` 里的 HTML 样式规范。

```bash
WECHAT_APPID=xxx WECHAT_SECRET=xxx python scripts/publish_draft.py \
  --title "标题" --digest "摘要" \
  --html 输出/content.html --cover 输出/cover.png \
  --img IMG1=路径/图1.png --img IMG2=路径/图2.png
```

- AppID/AppSecret 已配置在技能目录的 `.env` 文件（受 `.gitignore` 保护不提交）或系统环境变量中，脚本支持自动静默读取。
- 首次在某台电脑/某个网络使用：先去公众号后台「设置与开发 → 基本配置 → IP 白名单」加入当前公网 IP（用 `curl -s https://myip.ipip.net` 查；家庭宽带常有两个出口 IP，报错里会给真实 IP，以报错为准加白）。
- 常见错误：40164 = IP 不在白名单；40001 = Secret 错；48001 = 接口无权限。
- 正文图走 `/cgi-bin/media/uploadimg` 拿 mmbiz URL；封面走 `/cgi-bin/material/add_material` 拿 media_id。
- 推送成功后，草稿在「内容管理 → 草稿箱」。**群发必须本人在后台点发布**（订阅号需管理员扫码），任何工具都绕不过，不要尝试自动化最后一步。

## 第 5 步：发布检查清单

1. 标题 ≤ 21 字，摘要手写 ≤ 54 字，封面 2.35:1 文字不出血。
2. 开头 3 屏内有图，全文无超 3 句段落，图注齐全（12px 注释灰居中）。
3. 声明原创；新号不开赞赏。
4. 先发「预览」到自己微信通读一遍，再群发。
5. 群发时间：工作日 7:30 到 8:30 或 21:00 到 22:00。
6. 发完按 `references/cold-start-playbook.md` 的分发清单铺渠道。

## 换电脑迁移

1. 整个文件夹拷过去即可。
2. 目标机需要：Edge 或 Chrome（渲染图）、Python 3（脚本只用标准库，无需 pip 安装任何东西）。
3. 重新设置环境变量 WECHAT_APPID / WECHAT_SECRET，并把新网络的公网 IP 加进公众号后台白名单。

## 参考文件

- `references/style-rules.md`：文风硬规则 + 正文 HTML 内联样式规范
- `references/mdnice-theme.css`：mdnice 蓝金主题（手动排版时用）
- `references/cold-start-playbook.md`：冷启动运营方案（分发、互动、指标、排期）
