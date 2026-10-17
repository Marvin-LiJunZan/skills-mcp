---
name: claude-handoff
description: Hand the current conversation off to a fresh background agent that picks up the work immediately via claude --bg. Triggers on /claude-handoff, 后台交接, 启动后台Agent继续工作.
argument-hint: "What will the next session be used for?"
---

# Claude Background Handoff

Write a handoff summary of the current conversation so a fresh background agent can continue the work immediately without interrupting the user.

## Procedure

1. **Synthesize Session Context**:
   - High-level goal and background.
   - Work completed vs work remaining.
   - Key architectural decisions made.
   - Dead ends and avoided approaches.
   - Reference files and artifacts by path or URL (do not duplicate text).
   - Redact all secrets, passwords, or API keys.

2. **Launch Background Agent**:
   - Seed the new agent with the summary as its prompt:
     ```bash
     claude --bg --name "<descriptive name>" "<handoff summary>"
     ```
   - Always pass `-n` / `--name` with a descriptive name (e.g. `--name "Refactor auth middleware"`).
   - Starts in the current working directory and returns immediately.
   - Notify the user that the background agent has launched and can be inspected via `claude agents`.
