---
name: wechat-agent-bridge
description: WeChat personal protocol gateway and remote PC automation controller. Listens to WeChat group and direct messages, routes instructions to Antigravity/MCP agents by group topic, executes local tasks, and replies with files/results.
---

# WeChat Agent Bridge Skill (方案 2：个人微信协议框架)

Use this skill to remotely control your computer and trigger AI research/coding/export workflows directly from WeChat groups or private messages.

## System Architecture

```text
+-------------------+      QR Login / Token      +-------------------------+
| WeChat Mobile App | <========================> |  Gewechat / WeChat API  |
+-------------------+                            |  (Port 2531 / 2532)     |
        |                                        +-------------------------+
        | Send @Assistant Task                                | Webhook Forward
        v                                                     v
+--------------------------------------------------------------------------+
|                 Local Bridge Server (local_bridge.py)                    |
|  - Parse message & group context                                         |
|  - Match target task (Abaqus / Paper / Git / Video / Super-Resolution)   |
|  - Execute CLI / Antigravity Agent workflow                             |
|  - Return logs, images, or generated ZIP files back to WeChat chat       |
+--------------------------------------------------------------------------+
```

## Supported Tasks via WeChat
- **"跑仿真"**: Trigger Abaqus MCP model build and job submission.
- **"查文献 <关键词>"**: Call ccc-literature-scout or ArXiv search, returns PDF/BibTeX.
- **"增强图片"**: (Send blurry image with caption "高清化") -> Calls Real-ESRGAN/Lanczos, returns 4K image back into group.
- **"打包项目"**: Calls clean export and returns ready-to-share ZIP link/file.
- **"Git推送"**: Triggers automated Git commit & push.

## Configuration & Run

```powershell
# 1. Run local bridge service
py -3.11 skills/wechat-agent-bridge/scripts/local_bridge.py --port 8088
```
