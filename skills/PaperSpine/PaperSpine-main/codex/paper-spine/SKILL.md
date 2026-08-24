---
name: paper-spine
description: Use for PaperSpine paper and report writing workflows including intake, research, rewrite, build from materials, LaTeX output, translation, and audit.
---

# PaperSpine For Codex

Use this skill for any PaperSpine task in Codex. This is the Codex edition: one
official-style skill folder with all PaperSpine workflow logic, references, and
scripts bundled inside. Do not depend on separate child skills in Codex.

## Core Rule

PaperSpine is not a prose polisher. It must research the target scene, learn
strong examples, confirm the controlling motivation with the user, design the
writing unit by unit, and only then write, rewrite, build LaTeX, translate, and
audit.

Never fabricate data, metrics, citations, figures, experiments, or claims.
External papers teach structure and rhetoric only; user materials are the only
source for this manuscript's evidence.

## Mandatory Intake

Before starting a workflow, create config through the terminal wizard whenever
possible. In Claude Code, use `/paperspine`; it automatically launches the
intake UI when configuration is missing. `scripts/launch_paperspine_ui.ps1` is
the underlying launcher for the real interactive terminal window. The terminal
UI supports Up/Down option switching, Left/Right field switching, Enter
edit/confirm, and `S` save. Do not run the Python `input()` wizard inside hidden
Bash/tool execution.

```bash
python scripts/intake_wizard.py --output-dir paper_rewriting_output
```

The wizard must collect all config fields in the command line by numbered menus
or text input, show a final review screen, and allow editing before writing the
config. Do not ask the user to manually write JSON or answer a long plain chat
checklist unless the terminal is unavailable.

On first setup or when the user asks to change global preferences, run:

```bash
python scripts/intake_wizard.py --setup-global --output-dir paper_rewriting_output
```

Global setup records the command-line UI language preference (`zh` or `en`).

Required config fields:

| Field | Values |
|---|---|
| `workflow` | `rewrite_existing`, `build_from_materials` |
| `scene` | `journal`, `conference`, `report_review`, `competition` |
| `tier` | `flash`, `pro` |
| `output_language` | `en`, `zh` |
| `target_name` | free text |
| `materials_dir` | path or empty |
| `draft_path` | path or empty |
| `user_motivation` | hypothesis only; final motivation confirmed after research |
| `official_urls` | list |
| `special_requirements` | list |
| `word_output` | `none`, `docx` |
| `translation_package` | `none`, `zh` |
| `ui_language` | `zh`, `en` |

## Workflow

1. Run intake wizard and write `paper_spine_config.json` and `.md`.
2. Create or verify `source_map.md`.
3. Research before final motivation. Create `reference_materials/`,
   `research_dossier.md`, `exemplar_learning_dossier.md`, `style_profile.md`,
   `sota_gap_map.md`, and `motivation_options_after_research.md`.
4. Stop for user confirmation. Write `confirmed_motivation.md` only after the
   user chooses or revises the motivation.
5. For `rewrite_existing`, create `original_logic_map.md`, `evidence_bank.md`,
   `section_blueprints.md`, `writing_rationale_matrix.md`, `rewrite_matrix.md`,
   and `logic_transfer_audit.md` before final prose.
6. For `build_from_materials`, create `source_inventory.md`, `evidence_bank.md`,
   `figure_asset_map.md`, `claim_register.md`, `section_blueprints.md`, and
   `writing_rationale_matrix.md` before final prose.
7. Always produce `final_paper/main.tex`. Compile `paper.pdf` when a TeX engine
   is available. Markdown alone is not final.
8. If `word_output=docx`, produce `final_paper/paper.docx` and `word_report.md`.
9. If `output_language=en` and `translation_package=zh`, produce the full
   `translation_zh/` package. This means complete file-by-file translation of
   every required intermediate Markdown artifact, including large tables such as
   `writing_rationale_matrix.md`, plus a complete Chinese full-paper
   translation.
10. Run `artifact_check.py --markdown --write` before completion.

## Writing Rationale Matrix

`writing_rationale_matrix.md` is the writing plan, not a change log. It must be
much more detailed than simple rows such as "fix graphicspath" or "rewrite
abstract".

Use this table:

| Row ID | Manuscript Unit | Current Problem or Planned Function | Motivation Link | Reference/SOTA Pattern Learned | Target Scene or Venue Norm | User Evidence or Citation Anchor | Planned Change/Text Move | Final Text Check |
|---|---|---|---|---|---|---|---|---|

Rows must follow the real manuscript/report order and split the work into
paragraph-sized, claim-sized, evidence, model, synthesis, heading, caption, or
competition-solution units. A row should teach the user why the writing move is
better: what logic failed, what strong examples do, why the target venue expects
it, what evidence supports it, and how the final text should prove the claim.

The first row must be a deep whole-work framework row. It should explain the
chosen controlling structure, how SOTA/target examples informed that structure,
how the confirmed motivation orders later sections, which user evidence anchors
the arc, and how the final manuscript will be checked against it. Do not write a
one-line "conservation-first" or "problem-solution arc" summary without this
reasoning.

A generic row fails. Examples of failing reasons: "improve clarity", "polish",
"fix path", or "make abstract conservation-first" without detailed logic.

## Translation Package

When `translation_package=zh`, translate all required intermediate Markdown
artifacts and also produce:

- `translation_zh/writing_rationale_matrix.zh.md`: complete row-by-row Chinese
  translation of `writing_rationale_matrix.md`; preserve the full table and row
  count.
- `translation_zh/full_paper_translation.zh.md`: complete Chinese translation of
  the final paper text, including title, abstract, section prose, captions, table
  notes, limitations, and conclusion. Preserve citation keys, labels, formulas,
  file paths, and raw numeric values.
- `translation_zh/translation_coverage.md`: row-by-row coverage of every source
  artifact and every final-paper section/caption/table note.

Partial translation is a failed audit.

## References To Read As Needed

- `references/interactive-intake.md` for config and wizard behavior.
- `references/flash-pro-research.md` and `references/scenario-*.md` for target
  research.
- `references/writing-rationale-matrix.md` for detailed unit-by-unit planning.
- `references/build-from-materials.md` for from-zero construction.
- `references/rewrite-matrix.md` and `references/logic-transfer-audit.md` for
  rewrite work.
- `references/translation-package.md` for complete Chinese translation output.

## Scripts

Prefer bundled scripts over ad-hoc checks:

```bash
python scripts/intake_wizard.py --output-dir paper_rewriting_output
python scripts/material_inventory.py <materials_dir> --output-dir paper_rewriting_output
python scripts/artifact_check.py paper_rewriting_output --markdown --write
python scripts/latex_guard.py final_paper/main.tex --markdown
python scripts/word_guard.py final_paper/paper.docx --markdown
python scripts/revision_audit.py original.tex revised.tex --markdown
```
