#!/usr/bin/env python3
"""Sync PaperSpine release layouts and local installs.

The source tree keeps the Claude Code plugin layout. Exported release layouts
are split by host:

- `codex/paper-spine/`: single official-style Codex skill folder with `SKILL.md`.
- `claude-code/`: Claude Code plugin root with `.claude-plugin/` and `skills/`.

Local installs copy the single Codex skill into `.codex/skills/` and Claude flat
fallback skills into `.claude/skills/`. Claude command files are copied into
`.claude/commands/` so `/paperspine` and `/paperspine-ui` are available even
when the plugin itself has not been installed from a marketplace.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE_SKILLS = (
    "paper-spine",
    "paper-spine-intake",
    "paper-spine-research",
    "paper-spine-rewrite",
    "paper-spine-build",
    "paper-spine-latex",
    "paper-spine-audit",
)

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "paper_rewriting_output",
    "codex",
    "claude-code",
}
SKIP_FILES = {
    "DEPLOYED_TO_LOCAL_SKILLS.txt",
}


def parse_args() -> argparse.Namespace:
    home = Path.home()
    parser = argparse.ArgumentParser(description="Sync PaperSpine release layouts and local installs.")
    parser.add_argument(
        "--desktop-root",
        type=Path,
        default=home / "Desktop" / "PaperSpine",
        help="Desktop export root containing codex/ and claude-code/ versions.",
    )
    parser.add_argument(
        "--codex-skills-dir",
        type=Path,
        default=home / ".codex" / "skills",
        help="Codex skills directory. Receives the single paper-spine Codex skill.",
    )
    parser.add_argument(
        "--claude-skills-dir",
        type=Path,
        default=home / ".claude" / "skills",
        help="Claude Code flat skills directory for fallback direct discovery.",
    )
    parser.add_argument(
        "--claude-commands-dir",
        type=Path,
        default=home / ".claude" / "commands",
        help="Claude Code user commands directory. Receives PaperSpine slash commands.",
    )
    parser.add_argument(
        "--clean-legacy",
        action="store_true",
        help="Remove older nested/split PaperSpine exports and installs before syncing.",
    )
    parser.add_argument(
        "--clean-legacy-claude-nested",
        action="store_true",
        help="Deprecated alias for --clean-legacy.",
    )
    return parser.parse_args()


def ignore_repo_export(dir_path: str, names: list[str]) -> set[str]:
    ignored = {name for name in names if name in SKIP_DIRS or name in SKIP_FILES}
    ignored.update(name for name in names if name.endswith((".aux", ".log", ".out", ".toc")))
    return ignored


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_tree(src: Path, dest: Path, *, ignore=None) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=ignore)


def same_path(left: Path, right: Path) -> bool:
    try:
        return left.resolve() == right.resolve()
    except OSError:
        return left.absolute() == right.absolute()


def copy_plugin_root(target: Path) -> None:
    reset_dir(target)
    for item in ROOT.iterdir():
        if item.name in SKIP_DIRS or item.name in SKIP_FILES:
            continue
        dest = target / item.name
        if item.is_dir():
            copy_tree(item, dest, ignore=ignore_repo_export)
        else:
            shutil.copy2(item, dest)


def sync_flat_skills(skills_dir: Path) -> None:
    skills_dir.mkdir(parents=True, exist_ok=True)
    for skill in SUITE_SKILLS:
        copy_tree(ROOT / "skills" / skill, skills_dir / skill, ignore=ignore_repo_export)


def sync_codex_skill(skills_dir: Path) -> None:
    skills_dir.mkdir(parents=True, exist_ok=True)
    copy_tree(ROOT / "codex" / "paper-spine", skills_dir / "paper-spine", ignore=ignore_repo_export)


def sync_claude_commands(commands_dir: Path) -> None:
    commands_dir.mkdir(parents=True, exist_ok=True)
    source = ROOT / "commands"
    if not source.exists():
        return
    for command_file in source.glob("*.md"):
        shutil.copy2(command_file, commands_dir / command_file.name)


def export_desktop_versions(desktop_root: Path) -> None:
    if same_path(desktop_root, ROOT):
        print(f"Skipping desktop version export because target is the source tree: {desktop_root}")
        return
    reset_dir(desktop_root)
    copy_tree(ROOT / "codex", desktop_root / "codex", ignore=ignore_repo_export)
    copy_plugin_root(desktop_root / "claude-code")


def clean_legacy_paths(
    desktop_root: Path,
    codex_skills_dir: Path,
    claude_skills_dir: Path,
    claude_commands_dir: Path,
) -> None:
    paths = [
        desktop_root / "codex",
        desktop_root / "claude-code",
        codex_skills_dir / "PaperSpine",
        codex_skills_dir / "PaperSpineV2",
        claude_skills_dir / "PaperSpine",
        claude_skills_dir / "PaperSpineV2",
        claude_skills_dir / "paper-writing-assistant",
    ]
    paths.extend(codex_skills_dir / skill for skill in SUITE_SKILLS)
    paths.extend(claude_skills_dir / skill for skill in SUITE_SKILLS)
    paths.append(claude_commands_dir / "paperspine.md")
    paths.append(claude_commands_dir / "paperspine-ui.md")
    for path in paths:
        if path.exists():
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            except PermissionError as exc:
                print(f"Warning: skipped locked legacy path: {path} ({exc})", file=sys.stderr)


def main() -> int:
    args = parse_args()
    if args.clean_legacy or args.clean_legacy_claude_nested:
        clean_legacy_paths(
            args.desktop_root,
            args.codex_skills_dir,
            args.claude_skills_dir,
            args.claude_commands_dir,
        )

    export_desktop_versions(args.desktop_root)
    sync_codex_skill(args.codex_skills_dir)
    sync_flat_skills(args.claude_skills_dir)
    sync_claude_commands(args.claude_commands_dir)

    print("PaperSpine local sync complete")
    print(f"Desktop Codex version: {args.desktop_root / 'codex'}")
    print(f"Desktop Claude Code version: {args.desktop_root / 'claude-code'}")
    print(f"Codex single-skill install: {args.codex_skills_dir / 'paper-spine'}")
    print(f"Claude flat fallback install: {args.claude_skills_dir}")
    print(f"Claude command install: {args.claude_commands_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

