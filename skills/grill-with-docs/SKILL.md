---
name: grill-with-docs
description: A relentless interview to sharpen a plan or design against an existing codebase, creating and updating documentation (ADRs in docs/adr/ and GLOSSARY.md) as decisions are settled. Use when aligning a plan against a repository or codebase.
---

# Grill With Docs

A relentless interview to sharpen a plan or design against an existing codebase, persisting decisions and domain concepts into `GLOSSARY.md` and ADRs (`docs/adr/`) as you go.

---

## 1. The Interview Process

Follow the full Grilling protocol:
1. Map the plan or feature into a **design tree**.
2. Work the tree in **rounds** along the **frontier** (decisions whose prerequisites are settled).
3. Format each question with a numbered heading `❓ **Q1** - **<title>**:` and a concrete recommended answer `➡️ **Recommended**:`.
4. Let the user answer by number, recomputing the frontier after every turn.
5. Facts (file inspections, checking existing patterns or code) are your job—inspect the repository yourself or dispatch sub-agents; decisions are the user's.
6. The session finishes when the frontier is empty and the user explicitly confirms shared understanding.

---

## 2. Inline Domain Modeling & Documentation

As decisions settle during the interview:

### Update `GLOSSARY.md` Inline
- When the user uses a term that conflicts with existing language in `GLOSSARY.md`, call it out immediately.
- When ambiguous or overloaded terms arise, propose a precise canonical term.
- When a term is resolved, update `GLOSSARY.md` right away (do not wait until the end).
- Keep definitions tight: 1–2 sentences defining what the term IS, not what it does. List rejected terms under `_Avoid_`.

### Create Architecture Decision Records (ADRs) Sparingly
Create an ADR in `docs/adr/000X-<slug>.md` ONLY when all three criteria are met:
1. **Hard to reverse**: The cost of changing your mind later is meaningful.
2. **Surprising without context**: A future reader looking at the codebase would wonder why it was done this way.
3. **The result of a real trade-off**: There were genuine alternatives considered and rejected.

#### ADR Structure:
```md
# {Short title of the decision}

{1-3 sentences: context, what was decided, and why.}
```
