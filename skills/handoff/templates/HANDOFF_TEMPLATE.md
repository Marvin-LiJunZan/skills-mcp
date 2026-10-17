# Session Handoff Document

- **Created**: {{DATE_TIME}}
- **Harness / Agent**: {{AGENT_NAME}}
- **Repository / Directory**: `{{REPO_PATH}}`
- **Git Context**: `{{GIT_BRANCH}}` @ `{{GIT_COMMIT}}`
- **Next Session Objective**: {{NEXT_OBJECTIVE}}

---

## 1. Objective & Scope
<!-- Concise 2-4 sentence summary of what problem is being solved and why -->
{{OBJECTIVE_SUMMARY}}

## 2. Work Breakdown & Status
### Completed
- [x] {{COMPLETED_ITEM_1}} (see `{{FILE_PATH_1}}`)
- [x] {{COMPLETED_ITEM_2}}

### In-Flight / Paused
- [ ] {{IN_FLIGHT_ITEM_1}} - Current roadblock or state: {{DETAILS}}

## 3. Key Decisions & Rationale
<!-- The 'Why' behind non-obvious choices and trade-offs -->
- **Decision 1**: {{RATIONALE_1}}
- **Decision 2**: {{RATIONALE_2}}

## 4. Dead Ends & Rejected Approaches
<!-- Crucial section: Prevent next agent from retrying failed approaches -->
- **Attempt**: {{WHAT_WAS_TRIED}}
  - **Result**: {{WHY_IT_FAILED}}
  - **Learning**: {{KEY_TAKEAWAY}}

## 5. Key File Touchpoints
<!-- Relative file paths only, with brief notes on purpose -->
- `{{PATH_A}}`: {{PURPOSE_A}}
- `{{PATH_B}}`: {{PURPOSE_B}}

## 6. Immediate Next Steps
<!-- Ordered list of bite-sized, verifiable tasks -->
1. [ ] {{NEXT_STEP_1}}
2. [ ] {{NEXT_STEP_2}}
3. [ ] {{NEXT_STEP_3}}

## 7. Recommended Skills to Invoke
- `{{SKILL_NAME}}`: {{REASON_TO_INVOKE}}

## 8. Verification & Health Check
<!-- Commands the next session can run immediately to verify baseline health -->
```bash
{{TEST_OR_VERIFICATION_COMMAND}}
```
