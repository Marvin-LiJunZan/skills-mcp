---
name: grill-me
description: A relentless interview to stress-test and sharpen a plan, architecture, or idea. Interviews the user in structured rounds along the decision tree frontier, with recommendations and fact-finding sub-agents until reaching a shared understanding. Use when the user types /grill-me, asks to 'grill me', or wants to stress-test, clarify, or align on an idea or plan.
---

# Grill Me

A relentless interview to take a loose idea, plan, decision, or architecture and stress-test it until you can commit to it.

`grill-me` is **stateless**: it needs no repo setup, writes no files, and leaves no workspace artifacts behind. The only result is a crystal-clear version of the idea in your head, free of unstated assumptions.

---

## The Grilling Loop

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

### Question & Round Format

Format each round as a numbered list with clear recommendations:

```
❓ **Q1** - **<question title>**: <question body, explaining the trade-off or dilemma, with concrete options>

➡️ **Recommended**: <your recommended choice and concise rationale>

---

❓ **Q2** - **<question title>**: <question body, explaining the trade-off or dilemma, with concrete options>

➡️ **Recommended**: <your recommended choice and concise rationale>
```

The user can answer succinctly by question number (e.g. `1: A, 2: Recommended, 3: No, because...`).

---

## Core Rules & Mechanics

### 1. Recomputing the Frontier
Each round the user answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them.
- Recompute the frontier after each user response.
- Never ask a question in the current round that depends on another question still open in this round. Downstream questions belong to _later_ rounds.
- Later rounds should clearly build upon what the user decided in earlier rounds.

### 2. Facts vs. Decisions (Fact-Finding is Your Job)
- **Finding facts is YOUR job, never the user's**: When a frontier question needs information from the environment (codebase, files, search, docs, dependencies), look it up or dispatch a sub-agent to find it. Do not ask the user for anything you could inspect yourself.
- **Do not block on background fact-finding**: Running explorations are unsettled prerequisites—only the questions downstream of that fact wait. Ask the rest of the frontier now.
- **Decisions are the user's**: Lay out the trade-offs, provide your recommendation, and wait for the user's call. Never answer design decisions for the user without their input.

### 3. Avoid Passivity
- Grilling is a peer conversation, not a passive survey. Challenge weak premises, point out inconsistencies, and highlight hidden traps or edge cases.
- If the user simply nods along ("sounds good", "agreed") without real engagement, probe deeper into trade-offs and edge cases.
- If the user says "I don't know", treat that as a legitimate answer—it usually signals a need to prototype rather than debate.

### 4. Handling "Ungrillable" Questions
Some questions cannot be solved by talking (e.g. "How should the interaction feel?", UI styling, microscopic latency tuning).
- When a question cannot be resolved through conversation alone, call it out as ungrillable.
- Suggest a quick throwaway prototype or minimal spike to test it, then resume the interview once observed.

### 5. Termination Condition (Shared Understanding)
- The session is done when the **frontier is empty**: every branch of the design tree has been visited, and nothing remains silently assumed.
- **Confirmation Gate**: When the frontier is exhausted, summarize the settled design decisions and ask the user to confirm:
  > *"We have explored all open branches and reached the edge of the design tree. Do you confirm we have reached a shared understanding?"*
- **DO NOT start implementing or writing code until the user explicitly confirms.**

---

## Related Modes
- **Coding in a repository with docs**: If the user wants to persist decisions into `GLOSSARY.md` and ADR files (`docs/adr/`), switch to or invoke `grill-with-docs`.
- **One question at a time**: If the user prefers sequential questioning rather than batched rounds, adapt to asking one question per turn.
