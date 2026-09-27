# Research Project Template

面向研究生与 AI 助手协作的科研项目模板。

## 目录
- `paper/`：Elsevier LaTeX 论文
- `src/`：可复用源码
- `scripts/`：训练、数据处理与绘图脚本
- `data/raw/`：原始数据，只读
- `data/processed/`：处理后数据
- `configs/`：实验配置
- `results/`：指标、预测与日志
- `outputs/`：临时输出
- `docs/`：实验记录、说明文档

## 推荐工作流
1. 在 GitHub 或 Gitee 创建空仓库。
2. 将本模板作为项目起点。
3. 把仓库地址发给 AI 助手。
4. 对 AI 说：先检查 Git 状态并拉取最新版本。
5. 完成任务后，让 AI 汇总改动。
6. 确认后再提交并推送。

## 给 AI 的第一句话
```
这是我的科研项目仓库：[仓库地址]
请先克隆仓库并阅读 README.md 与 AGENTS.md。
告诉我项目结构和当前状态，暂时不要修改任何文件。
```

## 论文模板
`paper/main.tex` 使用 Elsevier `elsarticle` 单栏 preprint 模式。
图件默认按约 5 in 宽度设计，便于后续投稿版式调整。
具体格式以目标期刊最新 Guide for Authors 为准。
