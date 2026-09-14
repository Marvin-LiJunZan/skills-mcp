---
name: export-ai-conversations
description: Export locally stored AI assistant conversations and prompts from Antigravity, Codex, DeepSeek, WorkBuddy, and Cursor into Markdown with a unified index. Use for manual or scheduled daily backups; do not use for cloud-only histories that are not present on disk.
metadata:
  short-description: Export local AI conversations on a schedule
---

# Export AI conversations

Use the bundled script for the actual export. The script is deterministic and cheap to run: it reads local files/databases, converts recognized records to Markdown, and updates one index. Do not ask a language model to reformat every conversation.

## Default run

From PowerShell:

```powershell
python "C:\JunzanLi_project\skills_mcp\skills\export-ai-conversations\scripts\export_ai_conversations.py"
```

The default output is `C:\JunzanLi_project\skills_mcp\chats`. Override it when needed:

```powershell
python "C:\JunzanLi_project\skills_mcp\skills\export-ai-conversations\scripts\export_ai_conversations.py" --output "D:\AI\conversation-exports"
```

## Scheduled use

Schedule the command with Windows Task Scheduler, preferably once per day after the assistants have finished writing their local stores. Use `python` as the program and pass the full script path as the argument. Set the task to run whether or not the user is logged on only if the local application data is available to that account.

For a scheduled run, report only the counts and warnings printed by the script. A zero count for a source means that source was not found or had no parseable records; do not claim that its cloud history was exported.

## Operational rules

- Preserve existing files in the output directory. The script overwrites only files with its own stable prefixes and the generated index.
- Prefer `transcript_full.jsonl` over `transcript.jsonl` for Antigravity.
- Treat local stores as potentially changing while an app is open. If a database is locked or a JSONL line is incomplete, skip that record and report a warning; do not damage or rewrite source stores.
- Keep tool output bounded in Markdown so a single huge command result cannot make the daily archive unusable.
- This is a local-backup workflow. Do not upload conversation contents, call cloud APIs, or delete source data.

## Sources recovered from the previous export workflow

- Antigravity: `C:\Users\12830\.gemini\antigravity\brain\*\.system_generated\logs\transcript_full.jsonl` or `transcript.jsonl`
- Codex: `C:\Users\12830\.codex\sessions`, `C:\Users\12830\.codex\archived_sessions`, and `C:\Users\12830\.codex\session_index.jsonl`
- DeepSeek: `C:\JunzanLi_project\skills_mcp\chats\conversations.json` or `deepseek_data-*\conversations.json`
- WorkBuddy: `C:\Users\12830\AppData\Roaming\WorkBuddy\codebuddy-sessions.vscdb` and `C:\Users\12830\.workbuddy\brain`
- Cursor: `C:\Users\12830\AppData\Roaming\Cursor\User\workspaceStorage\*\state.vscdb`

