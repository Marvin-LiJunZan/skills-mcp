# PaperSpine

English | [中文](README.zh-CN.md)

PaperSpine is a motivation-driven skill suite for academic papers, competition
papers, technical reports, reviews, and other paper-like writing tasks.

It is not a one-shot polishing prompt. PaperSpine asks the agent to research the
target scene, learn from strong examples, confirm the controlling motivation,
design the manuscript unit by unit, write LaTeX, and audit the result.

## Core Idea

PaperSpine follows one principle:

> Learn first. Write later.

The workflow keeps the manuscript centered on motivation, evidence, structure,
and revision accountability. It is built for users who want to understand why a
paper is written in a certain way, not only receive a final draft.

## Features

- Four target scenes: `journal`, `conference`, `report/review`, `competition`.
- Two research tiers: `flash` and `pro`.
- Two workflows: rewrite an existing draft, or build from a materials folder.
- English or Chinese final output.
- Mandatory motivation confirmation after target-scene research.
- Required writing rationale matrix that explains the writing plan unit by unit.
- Mandatory LaTeX final output: `paper_rewriting_output/final_paper/main.tex`.
- PDF compilation when a TeX engine is available.
- Optional Word output checked by `word_guard.py`.
- Optional Chinese translation package after English output.
- Terminal intake UI with a welcome screen, arrow-key navigation, auto-filled
  project fields, and a browser preview server for visual testing.

## Repository Layout

PaperSpine supports Codex and Claude Code, but the install layouts are different.

```text
codex/paper-spine/        Codex single-skill layout
skills/                   Claude Code flat skill suite
commands/                 Claude Code slash-command helpers
.claude-plugin/           Claude Code plugin metadata
scripts/                  shared deterministic helpers
references/               shared workflow references
tests/                    local hardening tests
```

The repository root intentionally has no top-level `SKILL.md`. This prevents
duplicate or generic skill discovery.

## Codex Install

Codex should install the single official-style skill folder:

```text
codex/paper-spine
```

Windows PowerShell:

```powershell
git clone https://github.com/WUBING2023/PaperSpine.git "$HOME\PaperSpine"
New-Item -ItemType Directory -Force -Path "$HOME\.codex\skills"
Copy-Item -Recurse -Force "$HOME\PaperSpine\codex\paper-spine" "$HOME\.codex\skills\paper-spine"
```

macOS/Linux:

```bash
git clone https://github.com/WUBING2023/PaperSpine.git ~/PaperSpine
mkdir -p ~/.codex/skills
cp -R ~/PaperSpine/codex/paper-spine ~/.codex/skills/paper-spine
```

Restart Codex after installation. Invoke the skill with:

```text
$paper-spine
```

Expected Codex layout:

```text
~/.codex/skills/paper-spine/SKILL.md
~/.codex/skills/paper-spine/references/
~/.codex/skills/paper-spine/scripts/
```

Codex uses one bundled skill because Codex skill discovery works best with a
single self-contained folder for this project.

## Claude Code Install

Claude Code should use the plugin or the flat skill-suite layout. Do not install
`codex/paper-spine` as a Claude Code plugin.

### Plugin Install

```text
/plugin marketplace add https://github.com/WUBING2023/PaperSpine
/plugin install paper-spine
/reload-plugins
```

This exposes the suite skills:

```text
paper-spine
paper-spine-intake
paper-spine-research
paper-spine-rewrite
paper-spine-build
paper-spine-latex
paper-spine-audit
```

### Flat Skill Fallback

If you do not use the plugin system, copy the suite skills directly:

```bash
git clone https://github.com/WUBING2023/PaperSpine.git ~/PaperSpine
mkdir -p ~/.claude/skills ~/.claude/commands
cp -R ~/PaperSpine/skills/* ~/.claude/skills/
cp ~/PaperSpine/commands/*.md ~/.claude/commands/
```

On Windows PowerShell:

```powershell
git clone https://github.com/WUBING2023/PaperSpine.git "$HOME\PaperSpine"
New-Item -ItemType Directory -Force -Path "$HOME\.claude\skills", "$HOME\.claude\commands"
Copy-Item -Recurse -Force "$HOME\PaperSpine\skills\*" "$HOME\.claude\skills\"
Copy-Item -Force "$HOME\PaperSpine\commands\*.md" "$HOME\.claude\commands\"
```

Expected Claude Code flat layout:

```text
~/.claude/skills/paper-spine/SKILL.md
~/.claude/skills/paper-spine-intake/SKILL.md
~/.claude/skills/paper-spine-research/SKILL.md
~/.claude/commands/paperspine.md
```

After restart, the recommended command is:

```text
/paperspine
```

`/paperspine` starts PaperSpine and automatically launches the intake UI when
configuration is missing. `/paperspine-ui` is kept as a manual/legacy intake
launcher.

## Codex vs Claude Code

| Host | Recommended layout | Main invocation | Why |
|---|---|---|---|
| Codex | `codex/paper-spine` | `$paper-spine` | One bundled skill avoids duplicate discovery and includes all workflow logic. |
| Claude Code | plugin root or `skills/*` flat | `/paperspine` or the `paper-spine` skill | Claude Code discovers skills flat and can also use slash command helpers. |

## Intake UI

The intake wizard is a terminal UI. In Claude Code, `/paperspine` opens it in a
real PowerShell window so hidden tool execution does not block on stdin.

Keyboard controls:

- `Up/Down`: switch fields.
- `Left/Right`: switch options.
- `Enter`: edit or confirm.
- `S`: save.
- `Q`: quit.

The UI auto-fills project fields when possible, including draft paths, materials
folders, URLs, and default special requirements. The underlying configuration
field for the English-to-Chinese package is `translation_package`.

Visual preview:

```bash
python scripts/tui_preview_server.py --port 8765
```

Open `http://127.0.0.1:8765` and `http://127.0.0.1:8765/config`.

## Workflows

### Rewrite Existing

Use this when you already have a draft. PaperSpine creates:

- `original_logic_map.md`
- `research_dossier.md`
- `motivation_options_after_research.md`
- `confirmed_motivation.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`
- `rewrite_matrix.md`
- `logic_transfer_audit.md`
- `final_paper/main.tex`

### Build From Materials

Use this when you have notes, figures, data, reports, partial drafts, PDFs, or
experiment summaries but no complete paper.

PaperSpine creates:

- `source_inventory.md`
- `evidence_bank.md`
- `figure_asset_map.md`
- `claim_register.md`
- `research_dossier.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`
- `final_paper/main.tex`

## Research Tiers

- `flash`: 3 target-scene examples, 3 field examples, and official requirements.
- `pro`: 6 target-scene examples, 6 field examples, and official requirements.

Official requirements may come from journal author guidelines, conference CFPs,
school or department pages, course rubrics, competition websites, rule books,
templates, and official notices.

## Final Artifacts

PaperSpine treats LaTeX as the final required output:

```text
paper_rewriting_output/
  final_paper/
    main.tex
    paper.pdf        # when a TeX engine is available
    paper.docx       # optional
    figures/
  latex_report.md
  word_report.md     # when Word output is requested
  final_artifact_manifest.md
```

If no TeX compiler is available, `main.tex` is still required and
`latex_report.md` must record that compilation was skipped.

## Validation

Run the local test suite:

```bash
python -m unittest discover -s tests
```

Check output artifacts:

```bash
python scripts/artifact_check.py paper_rewriting_output --markdown --write
```

Optional checks:

```bash
python scripts/latex_guard.py paper_rewriting_output/final_paper/main.tex --markdown
python scripts/word_guard.py paper_rewriting_output/final_paper/paper.docx --markdown
```

## Local Development Sync

For maintainers working from a checkout:

```powershell
python scripts\sync_local_installs.py --clean-legacy
```

This exports the Codex and Claude Code release layouts and updates local
development installs.

## License

MIT License. See [LICENSE](LICENSE).
