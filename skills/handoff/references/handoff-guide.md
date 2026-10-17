# The Handoff Guide: Principles & Architecture

## 1. Why Handoff Exists
When working with AI coding agents (Claude Code, Antigravity, Codex, Cursor), sessions naturally accumulate context. Over 20-50+ turns, conversations suffer from:
1. **Context Rot & Token Bloat**: As token count rises, retrieval quality and adherence to instructions degrade.
2. **Tunnel Vision & Over-Fitting**: The agent becomes anchored on previous turns and mistakes.
3. **Session Barriers**: When you switch devices, restart the IDE, switch harnesses (e.g. from Antigravity to Claude Code), or delegate to a subagent, the live conversational buffer is lost.

`/handoff` provides **portability and clean state transitions**, packaging pure transit knowledge without carrying historical cruft.

---

## 2. The Four Memory Stores

A clean project architecture separates information into 4 distinct buckets:

| Store | Scope | Durability | Example |
| :--- | :--- | :--- | :--- |
| **Handoff Document** | Current transit task | Ephemeral (hours/days) | In-flight bugs, next 3 steps, failed attempts |
| **Project Docs** | Entire repository | Permanent | `README.md`, `CONTEXT.md`, ADRs, Architecture specs |
| **Issue Tracker** | Team tasks | Semi-permanent | GitHub Issues, Linear tickets, `.taskmd` |
| **Agent Memory** | Machine / Agent | User-scoped | User coding preferences, custom environment settings |

**Rule of Thumb:**
- Never duplicate in the Handoff document what belongs in Project Docs or the Issue Tracker. Reference by path.
- Keep the Handoff document strictly focused on: *Where are we right now, what failed, and what should be done next?*

---

## 3. Anti-Patterns to Avoid

1. **The Novel / Log Dump**: Pasting pages of code or chat history.
   * *Fix*: Link to the file and commit hash.
2. **The "Everything is Done" Falsehood**: Stating assumptions as facts.
   * *Fix*: Mark tested facts as `[VERIFIED]`, and untested beliefs as `[ASSUMED / UNVERIFIED]`.
3. **Credential Leaks**: Forgetting to redact secrets.
   * *Fix*: Automatically scrub `.env` values, API keys (`sk-...`, `Bearer ...`).
4. **Neglecting Dead Ends**: Leaving out what failed.
   * *Fix*: Always document rejected paths. It saves the next agent from burning tokens rediscovering the same failure.
