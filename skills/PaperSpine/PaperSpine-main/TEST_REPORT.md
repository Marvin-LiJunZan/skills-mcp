# PaperSpine v2 Local Hardening Test Report

Status: local release-candidate hardening, not pushed to GitHub.

## Scope

This report covers local validation of the PaperSpine v2 skill suite after the
Claude Code-compatible single-layout change and the latest writing-quality
hardening pass.

Validated areas:

- flat suite skill layout under `skills/*`,
- absence of a root `SKILL.md` to avoid duplicate Codex discovery,
- Claude Code plugin manifest,
- README installation and troubleshooting instructions,
- intake wizard,
- material inventory,
- artifact completeness checker,
- Word output validator,
- LaTeX/style/revision scripts,
- install layout simulation,
- local sync script safety,
- privacy and repository hygiene checks.

## Latest Quality Hardening

The latest pass changes PaperSpine from a surface-level rewriting helper into a
research-then-design workflow shared by both `rewrite_existing` and
`build_from_materials`.

Key enforced rules:

- Research happens before final motivation selection.
- User motivation given at intake is treated as a hypothesis until research is
  complete.
- `paper-spine-research` must create `reference_materials/`,
  `research_dossier.md`, `exemplar_learning_dossier.md`, `style_profile.md`,
  `sota_gap_map.md`, and `motivation_options_after_research.md`.
- The user must confirm the controlling motivation before drafting or rewriting.
- Both build and rewrite workflows must create `writing_rationale_matrix.md`
  before final prose.
- `writing_rationale_matrix.md` is scene-flexible: it must split the work into
  paragraph-sized, claim-sized, evidence, model, synthesis, heading, caption, or
  competition-solution units as needed, not force every task into a fixed IMRaD
  template.
- `artifact_check.py` now checks the matrix content, including overall framework
  row, required rationale columns, minimum row count, and generic/empty cells.
- The rationale matrix must proceed in manuscript order: whole-paper framework,
  abstract, every Introduction paragraph, Methods units, Results evidence units,
  Discussion/Conclusion paragraphs, and argument-bearing headings/captions.
- Each rationale row must connect the writing decision to motivation, learned
  SOTA/example patterns, target-scene norms, user evidence/citation anchors, and
  final text checks.
- English outputs with `translation_package: zh` must translate the complete
  intermediate artifact set and the final result reading package, not only a
  subset.
- Reference/downloaded materials must live under
  `paper_rewriting_output/reference_materials/` with a `source_index.md`.

## Commands Run

```bash
python -m unittest discover -s tests
python -m compileall scripts skills tests
claude plugin validate .
rg -n "<private-path-or-historical-project-patterns>" .
```

The unit suite also exercises these paths internally:

```bash
python scripts/intake_wizard.py --no-interactive ...
python scripts/material_inventory.py ...
python scripts/artifact_check.py ... --markdown --write
python scripts/word_guard.py ... --markdown
python scripts/style_metrics.py ... --markdown
python scripts/revision_audit.py ... --markdown
python scripts/latex_guard.py ... --markdown
python scripts/sync_local_installs.py --clean-legacy ...
```

## Results

| Area | Result | Notes |
|---|---|---|
| Unit tests | PASS | 38 tests passed. |
| Python compile check | PASS | Root scripts, suite scripts, and tests compile. |
| Claude Code plugin manifest | PASS | `claude plugin validate` passed. |
| Root duplicate guard | PASS | Root `SKILL.md` is absent by design. |
| Codex release layout | PASS | Top-level `codex/` contains a single official-style `paper-spine` skill bundling all workflows. |
| Claude Code release layout | PASS | Repository root and desktop `claude-code/` export validate as Claude Code plugin roots. |
| Intake wizard | PASS | Rewrite/build, flash/pro, English/Chinese, Word option, and translation package paths covered. |
| Material inventory | PASS | Images, PDFs, Word/text, LaTeX, data, and code files classify correctly. |
| Artifact check | PASS | Missing artifacts fail; final LaTeX is mandatory; PDF and Word policies are enforced. |
| Translation package check | PASS | English + Chinese package requires all common and workflow-specific translated MD artifacts. |
| Reference material workspace | PASS | `reference_materials/source_index.md` is a required artifact. |
| Rationale matrix check | PASS | `writing_rationale_matrix.md` is a required artifact for both workflows. |
| Word guard | PASS | Requested Word output requires `paper.docx` and `word_report.md`. |
| Existing scripts | PASS | LaTeX, style, and revision smoke tests pass. |
| Install simulation | PASS | Codex package and Claude flat fallback layouts are generated in temporary directories. |
| Sync safety | PASS | Sync script does not delete the source tree when the desktop target equals the source tree. |
| Privacy scan | PASS | No private path, target venue, local file URL, or historical manuscript-version terms found. |
| Codex parse guard | PASS | `SKILL.md` metadata files are UTF-8 without BOM so frontmatter starts at byte 1. |

## Fixes Made During This Pass

- Updated tests for the current no-root-`SKILL.md` design.
- Updated README to remove stale root-wrapper installation instructions.
- Added source-tree safety to `scripts/sync_local_installs.py`.
- Removed local deployment records containing machine paths from the reusable
  source tree.
- Extended artifact tests to require research-after-intake artifacts,
  reference material indexing, `writing_rationale_matrix.md`, and complete
  translation-package coverage.
- Verified Claude plugin metadata after the documentation and structure changes.
- Cleaned generated `__pycache__` directories after test and compile runs.
- Restored two host-specific release layouts: `codex/` as a single official-style Codex skill and Claude Code plugin layout for Claude Code.
- Removed UTF-8 BOM from PaperSpine metadata/text files; Codex appears to skip `SKILL.md` when frontmatter is preceded by BOM bytes.

## Remaining Manual Checks

These require real host application behavior and were not claimed as automated:

- restart Codex and confirm the slash menu shows one entry per PaperSpine skill;
- restart Claude Code and confirm plugin skill discovery through `/plugin install`;
- run a full real manuscript workflow and inspect whether the rationale matrix
  actually drives substantive section-level rewrites.

## Release Readiness

The local suite is structurally ready for a release-candidate test. The main
remaining risk is qualitative rather than structural: real paper runs must be
reviewed to confirm that the rationale matrix is being used as the drafting plan,
not generated as a superficial post-hoc explanation.




