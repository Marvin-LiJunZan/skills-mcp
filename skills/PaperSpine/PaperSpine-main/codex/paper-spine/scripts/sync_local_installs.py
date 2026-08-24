#!/usr/bin/env python3
"""Sync PaperSpine release layouts and local installs.

The source tree keeps the Claude Code plugin layout. Exported release layouts
are split by host:

- `codex/`: Codex official-style flat skill folders, each with `SKILL.md`.
- `claude-code/`: Claude Code plugin root with `.claude-plugin/` and `skills/`.

Local installs copy Codex skills flat into `.codex/skills/` and Claude flat
fallback skills into `.claude/skills/`.
"""

from __future__ import annotations

import argparse
import shutil
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
        help="Codex skills directory. Receives official-style flat skill folders.",
    )
    parser.add_argument(
        "--claude-skills-dir",
        type=Path,
        default=home / ".claude" / "skills",
        help="Claude Code flat skills directory for fallback direct discovery.",
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


def export_desktop_versions(desktop_root: Path) -> None:
    if same_path(desktop_root, ROOT):
        print(f"Skipping desktop version export because target is the source tree: {desktop_root}")
        return
    reset_dir(desktop_root)
    sync_flat_skills(desktop_root / "codex")
    copy_plugin_root(desktop_root / "claude-code")


def clean_legacy_paths(desktop_root: Path, codex_skills_dir: Path, claude_skills_dir: Path) -> None:
    paths = [
        desktop_root / "codex",
        desktop_root / "claude-code",
        codex_skills_dir / "PaperSpine",
        codex_skills_dir / "PaperSpineV2",
        claude_skills_dir / "PaperSpine",
        claude_skills_dir / "PaperSpineV2",
    ]
    paths.extend(codex_skills_dir / skill for skill in SUITE_SKILLS)
    paths.extend(claude_skills_dir / skill for skill in SUITE_SKILLS)
    for path in paths:
        if path.exists():
            shutil.rmtree(path)


def main() -> int:
    args = parse_args()
    if args.clean_legacy or args.clean_legacy_claude_nested:
        clean_legacy_paths(args.desktop_root, args.codex_skills_dir, args.claude_skills_dir)

    export_desktop_versions(args.desktop_root)
    sync_flat_skills(args.codex_skills_dir)
    sync_flat_skills(args.claude_skills_dir)

    print("PaperSpine local sync complete")
    print(f"Desktop Codex version: {args.desktop_root / 'codex'}")
    print(f"Desktop Claude Code version: {args.desktop_root / 'claude-code'}")
    print(f"Codex flat install: {args.codex_skills_dir}")
    print(f"Claude flat fallback install: {args.claude_skills_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
