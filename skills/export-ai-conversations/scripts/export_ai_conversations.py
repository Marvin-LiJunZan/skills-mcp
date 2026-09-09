"""Export local AI assistant records to Markdown without network access."""

from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sqlite3
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

TZ = timezone(timedelta(hours=8))
ROOT = Path(r"C:\JunzanLi_project\skills_mcp")
DEFAULT_OUTPUT = ROOT / "chats"
MAX_TOOL_OUTPUT = 5000


def text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=2)


def local_time(value):
    if not value:
        return "未知时间", datetime.min.replace(tzinfo=TZ)
    try:
        if isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(value, tz=timezone.utc).astimezone(TZ)
            return dt.strftime("%Y-%m-%d %H:%M:%S"), dt
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        dt = dt.astimezone(TZ)
        return dt.strftime("%Y-%m-%d %H:%M:%S"), dt
    except Exception:
        return str(value), datetime.min.replace(tzinfo=TZ)


def clean_title(value, fallback):
    value = re.sub(r"<[^>]+>", " ", text(value))
    value = re.sub(r"[\\/:*?\"<>|\r\n\t#*`]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip(" ._")
    return (value[:50] or fallback)


def filename(value):
    return re.sub(r"[\\/:*?\"<>|\r\n]+", "_", value).strip(" .")[:80]


def read_jsonl(path):
    rows = []
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return rows


def md_header(app, title, record_id, created, extra=None):
    lines = [f"# [{app}] 对话记录: {title}", "", f"- **平台 / 应用**: `{app}`", f"- **会话 ID**: `{record_id}`", f"- **创建时间 (UTC+8)**: {created}"]
    if extra:
        lines.extend(f"- **{key}**: `{value}`" for key, value in extra.items() if value)
    return lines + ["", "---", ""]


def export_antigravity(output):
    base = Path(r"C:\Users\12830\.gemini\antigravity\brain")
    count = 0
    if not base.exists():
        return count
    for conv in base.iterdir():
        logs = conv / ".system_generated" / "logs"
        full, short = logs / "transcript_full.jsonl", logs / "transcript.jsonl"
        source = full if full.is_file() and full.stat().st_size else short
        if not source.is_file():
            continue
        rows = read_jsonl(source)
        if not rows:
            continue
        created, created_dt = local_time(rows[0].get("created_at"))
        first = next((r.get("content", "") for r in rows if r.get("type") == "USER_INPUT" and r.get("content")), "")
        title = clean_title(first.splitlines()[0] if first else "", f"会话_{conv.name[:8]}")
        lines = md_header("Antigravity", title, conv.name, created, {"步骤数": len(rows)})
        for row in rows:
            stamp, _ = local_time(row.get("created_at"))
            kind, source_name, content = row.get("type", ""), row.get("source", ""), text(row.get("content", ""))
            if kind == "USER_INPUT":
                lines += [f"## 👤 用户提问 ({stamp})", "", content, "", "---", ""]
            elif source_name == "MODEL" or kind == "PLANNER_RESPONSE":
                lines += [f"## 🤖 助手回答 ({stamp})", "", content, "", "---", ""]
            elif kind in {"RUN_COMMAND", "VIEW_FILE", "GREP_SEARCH", "LIST_DIRECTORY", "CODE_ACTION", "SEARCH_WEB", "READ_URL_CONTENT"}:
                clipped = content[:MAX_TOOL_OUTPUT]
                lines += [f"<details><summary>🔧 工具执行结果: {kind}</summary>", "", "```text", clipped, "```", "</details>", ""]
        (output / f"Antigravity_{created_dt.strftime('%Y-%m-%d_%H%M%S')}_{filename(title)}_{conv.name[:8]}.md").write_text("\n".join(lines), encoding="utf-8")
        count += 1
    return count


def export_codex(output):
    roots = [Path(r"C:\Users\12830\.codex\sessions"), Path(r"C:\Users\12830\.codex\archived_sessions")]
    titles = {}
    index = Path(r"C:\Users\12830\.codex\session_index.jsonl")
    for row in read_jsonl(index) if index.is_file() else []:
        if row.get("id"):
            titles[row["id"]] = row.get("thread_name", "")
    count = 0
    paths = {p for root in roots if root.exists() for p in root.rglob("*.jsonl")}
    for path in paths:
        rows = read_jsonl(path)
        meta = next((r for r in rows if r.get("type") == "session_meta"), {})
        payload = meta.get("payload", {}) if isinstance(meta.get("payload", {}), dict) else {}
        sid = payload.get("id") or path.stem
        created, created_dt = local_time(payload.get("created_at") or meta.get("timestamp"))
        title = payload.get("thread_name") or titles.get(sid) or ""
        dialogue = []
        for row in rows:
            p = row.get("payload", {})
            if not isinstance(p, dict):
                continue
            stamp, _ = local_time(row.get("timestamp"))
            kind = p.get("type")
            if kind == "message":
                pieces = p.get("content", [])
                body = "\n".join(text(x.get("text", "") if isinstance(x, dict) else x) for x in pieces).strip()
                if p.get("role") in {"user", "assistant"} and body:
                    dialogue.append((p["role"], stamp, body))
                    if not title and p["role"] == "user":
                        title = body.splitlines()[0]
            elif kind in {"function_call", "function_call_output", "reasoning"}:
                dialogue.append((kind, stamp, text(p.get("arguments") or p.get("output") or p.get("summary", ""))))
        if not dialogue:
            continue
        title = clean_title(title, f"Codex会话_{str(sid)[:8]}")
        lines = md_header("Codex", title, sid, created, {"消息数": len(dialogue), "工作区路径": payload.get("cwd", "")})
        for role, stamp, body in dialogue:
            if role == "user":
                lines += [f"## 👤 用户提问 ({stamp})", "", body, "", "---", ""]
            elif role == "assistant":
                lines += [f"## 🤖 Codex 回答 ({stamp})", "", body, "", "---", ""]
            else:
                lines += [f"<details><summary>🔧 {role}</summary>", "", "```text", body[:MAX_TOOL_OUTPUT], "```", "</details>", ""]
        (output / f"Codex_{created_dt.strftime('%Y-%m-%d_%H%M%S')}_{filename(title)}_{str(sid)[:8]}.md").write_text("\n".join(lines), encoding="utf-8")
        count += 1
    return count


def export_deepseek(output):
    chats = Path(r"C:\JunzanLi_project\skills_mcp\chats")
    candidates = [chats / "conversations.json", *chats.glob("deepseek_data-*/conversations.json")]
    source = next((p for p in candidates if p.is_file()), None)
    if not source:
        return 0
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except Exception:
        return 0
    if not isinstance(data, list):
        return 0
    count = 0
    for conv in data:
        cid = str(conv.get("id") or conv.get("conversation_id") or "unknown")
        title = clean_title(conv.get("title") or conv.get("name"), f"DeepSeek会话_{cid[:8]}")
        created, created_dt = local_time(conv.get("created_at") or conv.get("createdAt"))
        lines = md_header("DeepSeek", title, cid, created)
        messages = conv.get("messages") or conv.get("msgs") or []
        if isinstance(messages, dict):
            messages = list(messages.values())
        for msg in messages if isinstance(messages, list) else []:
            role = msg.get("role") or msg.get("sender") or "assistant"
            body = msg.get("content") or msg.get("text") or msg.get("message") or ""
            if isinstance(body, list):
                body = "\n".join(text(x) for x in body)
            stamp, _ = local_time(msg.get("created_at") or msg.get("inserted_at"))
            label = "用户提问" if role in {"user", "human"} else "DeepSeek 回答"
            lines += [f"## {'👤' if role in {'user', 'human'} else '🤖'} {label} ({stamp})", "", text(body), "", "---", ""]
        (output / f"DeepSeek_{created_dt.strftime('%Y-%m-%d_%H%M%S')}_{filename(title)}_{cid[:8]}.md").write_text("\n".join(lines), encoding="utf-8")
        count += 1
    return count


def export_workbuddy(output):
    db = Path(r"C:\Users\12830\AppData\Roaming\WorkBuddy\codebuddy-sessions.vscdb")
    if not db.is_file():
        return 0
    count = 0
    try:
        conn = sqlite3.connect(f"file:{urllib.parse.quote(str(db))}?mode=ro", uri=True)
        rows = conn.execute("SELECT value FROM ItemTable").fetchall()
        conn.close()
    except sqlite3.Error:
        return 0
    for (value,) in rows:
        try:
            item = json.loads(value.decode("utf-8", "ignore") if isinstance(value, bytes) else value)
        except Exception:
            continue
        if not isinstance(item, dict) or not item.get("conversationId"):
            continue
        cid = str(item["conversationId"])
        title = clean_title(item.get("title") or item.get("customTitle"), f"WorkBuddy会话_{cid[:8]}")
        created, created_dt = local_time((item.get("createdAt") or 0) / 1000 if item.get("createdAt") else "")
        lines = md_header("WorkBuddy", title, cid, created, {"状态": item.get("status", "")})
        lines += ["## 👤 用户任务主题 / 提示词", "", title, ""]
        (output / f"WorkBuddy_{created_dt.strftime('%Y-%m-%d_%H%M%S')}_{filename(title)}_{cid[:8]}.md").write_text("\n".join(lines), encoding="utf-8")
        count += 1
    return count


def export_cursor(output):
    base = Path(r"C:\Users\12830\AppData\Roaming\Cursor\User\workspaceStorage")
    if not base.exists():
        return 0
    count = 0
    for ws in base.iterdir():
        db = ws / "state.vscdb"
        if not db.is_file():
            continue
        try:
            conn = sqlite3.connect(f"file:{urllib.parse.quote(str(db))}?mode=ro", uri=True)
            row = conn.execute("SELECT value FROM ItemTable WHERE key='aiService.prompts'").fetchone()
            conn.close()
            prompts = json.loads(row[0].decode("utf-8", "ignore") if isinstance(row and row[0], bytes) else row[0]) if row else []
        except Exception:
            continue
        if not isinstance(prompts, list) or not prompts:
            continue
        title = clean_title(ws.name, "工作区")
        lines = md_header("Cursor", f"工作区: {title}", ws.name, "历史保存记录", {"Prompt数": len(prompts)})
        for i, prompt in enumerate(prompts, 1):
            body = prompt.get("text", "") if isinstance(prompt, dict) else text(prompt)
            lines += [f"### 💬 历史提问 #{i}", "", body, "", "---", ""]
        (output / f"Cursor_工作区_{filename(title)}_{ws.name[:8]}.md").write_text("\n".join(lines), encoding="utf-8")
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description="Export local AI assistant conversations to Markdown")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    counts = {
        "Antigravity": export_antigravity(output),
        "DeepSeek": export_deepseek(output),
        "Codex": export_codex(output),
        "WorkBuddy": export_workbuddy(output),
        "Cursor": export_cursor(output),
    }
    total = sum(counts.values())
    index = ["# AI 对话与 Prompt 历史归档全集", "", f"- **更新时间 (UTC+8)**: {datetime.now(TZ):%Y-%m-%d %H:%M:%S}", f"- **总归档数**: {total}", ""]
    index += ["| 应用 | 导出数量 |", "|---|---:|"]
    index += [f"| {app} | {n} |" for app, n in counts.items()]
    (output / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "total": total, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
