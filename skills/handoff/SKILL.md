---
name: handoff
description: Transfers working context between AI sessions and agents (Claude Code, Antigravity, Codex, Cursor, etc.), prevents context degradation, creates clean session checkpoints, and handles session resumption. Triggers on /handoff, 做个handoff, 会话交接, 跨会话交接, 保存当前状态, 恢复会话, resume handoff, reconcile.
argument-hint: "What will the next session be used for? Or mode: create | resume | status | close | reconcile"
---

# Handoff Skill: Multi-Agent & Cross-Session Context Transfer

The `handoff` skill captures the current session's live context—in-flight work, architectural decisions, dead ends, and immediate next steps—into a clean, portable **handoff document** so a fresh agent session or different model harness can pick up work seamlessly without context rot, token explosion, or duplicated effort.

---

## 1. When to Use This Skill

Trigger this skill whenever:
- **Context window is filling up** or conversation is getting long/sluggish (preventing hallucinations and context degradation).
- **Session boundary reached**: pausing work, wrapping up for the day, or switching to another task.
- **Switching agents or harnesses**: moving from Antigravity to Claude Code, Codex, Cursor, or delegating to a background subagent.
- **Forking a side task**: creating a clean snapshot for a side investigation or prototype while keeping the main track clear.
- **Resuming work**: picking up where a previous session or colleague left off.
- **Reconciling state**: updating project documentation and tracker lists to reflect code changes.

**User Trigger Examples:**
- `/handoff` or `/handoff create [notes]`
- `/handoff resume [path]`
- `/handoff status`
- `/handoff close`
- `/handoff reconcile`
- "做个 handoff", "交接当前会话", "保存当前进度供新会话继续", "读取上次 handoff 继续工作"

---

## 2. Core Operational Modes

### Mode 1: Create (`/handoff` or `/handoff create`) [Default]

When invoked without an explicit mode argument or with `create`:
1. **Analyze the Live Session**:
   - Inspect git status (`git status -s`, recent commit diffs).
   - Identify the user's overarching goal.
   - Summarize what has been completed in this session vs. what is mid-flight.
   - Record key architectural and technical decisions made and their rationale.
   - Document **dead ends and rejected attempts** (critical so the next agent doesn't repeat failed approaches).
2. **Strict Privacy & Secret Redaction**:
   - NEVER output API keys, bearer tokens, passwords, private keys, or sensitive credentials. Redact as `<REDACTED_API_KEY>`.
3. **Reference Artifacts, Do Not Duplicate**:
   - Reference files, specs, test files, and diffs by relative path or line numbers. Avoid pasting massive blocks of existing file contents.
4. **Determine Target Location**:
   - Preferred project path: `.handoff/HANDOFF_LATEST.md` (or `.handoff/HANDOFF_<timestamp>.md`).
   - If project is not tracked or user prefers external: OS temporary directory (`%TEMP%\handoff_<session>.md` on Windows, `/tmp/handoff_<session>.md` on Unix).
   - Ensure the target directory exists before writing.
5. **Include "Suggested Skills"**:
   - Explicitly list recommended skills for the next agent (e.g., `tdd`, `code-review`, `figma-use`, `academic-figure-skill`, `tex-to-word-converter`, etc.).
6. **Report to User**:
   - Print a concise handoff card and the exact file path so the user can easily point the next session to it.

---

### Mode 2: Resume (`/handoff resume [optional_path]`)

When invoked to resume or pick up a handoff:
1. **Locate the Handoff Document**:
   - If a path is provided, read that file.
   - Otherwise, look for `.handoff/HANDOFF_LATEST.md` in the current workspace, or scan the OS temp directory for the most recent handoff file.
2. **Run Zero-Assumption Verification (Reality Check)**:
   - Do NOT blindly trust claims in the document.
   - Verify:
     * Does the git branch match?
     * Do the referenced files actually exist and contain expected changes?
     * Run quick diagnostic tests or build checks if applicable.
   - Mark any discrepancy between the document and actual disk state as `[CORRECTED]`.
3. **Present Briefing to User**:
   - Goal & Current Milestone.
   - Immediate Next Tasks (numbered action checklist).
   - Suggested skills activated.
4. **Transition to Execution**:
   - Ask for confirmation or begin working immediately on the first pending task.

---

### Mode 3: Status (`/handoff status`)

- Read-only inspection.
- Reads `.handoff/HANDOFF_LATEST.md` or active handoff file without modifying files or taking actions.
- Displays summary of active in-flight goals, pending items, and last updated timestamp.

---

### Mode 4: Close (`/handoff close`)

- Invoked when a task is completed and no further continuation is required.
- Reconciles project tracker or checklist docs.
- Archives `.handoff/HANDOFF_LATEST.md` to `.handoff/archive/HANDOFF_<timestamp>.md`.
- Clears the active handoff file so future sessions start cleanly.

---

### Mode 5: Reconcile (`/handoff reconcile`)

- A mid-session alignment sweep.
- Checks durable project documents (`README.md`, `CONTEXT.md`, task checklists, issue trackers) against code modified in the session.
- Updates status markers (e.g. changing `[ ]` to `[x]`, updating API signatures or docstrings).
- Leaves the handoff file untouched.

---

## 3. Standard Handoff Document Schema

When generating a handoff document, format it as follows:

```markdown
# Session Handoff Document

- **Created At**: YYYY-MM-DD HH:MM:SS
- **Working Directory**: /path/to/project
- **Git Branch / Commit**: branch-name (commit-hash)
- **Target / Next Session Objective**: [Specific goal for next session]

## 1. High-Level Goal & Context
Brief summary of what this project/task is attempting to accomplish.

## 2. Progress Breakdown
- [x] Completed items with file references
- [ ] In-flight items with current status and blocking points

## 3. Key Technical Decisions & Architecture (The "Why")
- Decision 1: Reason and trade-offs.
- Decision 2: Architectural choice made.

## 4. Dead Ends & What NOT to Do
- Failed Attempt 1: What was tried and why it failed. Prevents repeating mistakes.

## 5. Touchpoint Files
- `path/to/file1.ext`: Purpose / modifications.
- `path/to/file2.ext`: Relevant test or config.

## 6. Immediate Next Steps (Priority Order)
1. Step 1: Specific, actionable instruction.
2. Step 2: Next verification or implementation step.

## 7. Suggested Skills for Next Agent
- `skill-name-1`: Why to use it.
- `skill-name-2`: Why to use it.

## 8. Verification & Test Commands
- Command to run tests: `...`
- Health check: `...`
```

---

## 4. Cross-Agent Best Practices

1. **Be Concise & Signal-Dense**: Avoid filler. Use bullet points and precise references.
2. **Never Duplicate Settled Detail**: If an ADR, PR description, or spec exists, link to it by path or URL.
3. **No Blind Contracts**: Clearly differentiate `[VERIFIED: tested on disk]` from `[ASSUMED / UNVERIFIED]`.
4. **Durable vs Ephemeral**: Keep permanent facts in repo docs (`README.md`, `CONTEXT.md`), and reserve handoff docs strictly for ephemeral transit state.
