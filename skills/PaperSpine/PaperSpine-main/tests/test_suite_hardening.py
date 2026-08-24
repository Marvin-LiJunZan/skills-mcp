from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUITE_SKILLS = [
    "paper-spine",
    "paper-spine-intake",
    "paper-spine-research",
    "paper-spine-rewrite",
    "paper-spine-build",
    "paper-spine-latex",
    "paper-spine-audit",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def frontmatter_field(text: str, field: str) -> str:
    match = re.search(rf"^{field}:\s*(.+)$", text, flags=re.MULTILINE)
    if not match:
        raise AssertionError(f"Missing frontmatter field: {field}")
    return match.group(1).strip()


class SuiteHardeningTests(unittest.TestCase):
    def test_suite_skill_names_are_unique_and_match_directories(self) -> None:
        names: list[str] = []
        for skill in SUITE_SKILLS:
            text = read(f"skills/{skill}/SKILL.md")
            name = frontmatter_field(text, "name")
            self.assertEqual(name, skill)
            names.append(name)
        self.assertEqual(len(names), len(set(names)))

    def test_script_copies_match_root_versions(self) -> None:
        copies = {
            "scripts/intake_wizard.py": [
                "skills/paper-spine/scripts/intake_wizard.py",
                "skills/paper-spine-intake/scripts/intake_wizard.py",
            ],
            "scripts/launch_paperspine_ui.ps1": [
                "skills/paper-spine/scripts/launch_paperspine_ui.ps1",
                "skills/paper-spine-intake/scripts/launch_paperspine_ui.ps1",
            ],
            "scripts/material_inventory.py": [
                "skills/paper-spine/scripts/material_inventory.py",
                "skills/paper-spine-build/scripts/material_inventory.py",
            ],
            "scripts/artifact_check.py": [
                "skills/paper-spine/scripts/artifact_check.py",
                "skills/paper-spine-audit/scripts/artifact_check.py",
            ],
            "scripts/word_guard.py": [
                "skills/paper-spine-latex/scripts/word_guard.py",
                "skills/paper-spine-audit/scripts/word_guard.py",
            ],
            "scripts/latex_guard.py": [
                "skills/paper-spine-latex/scripts/latex_guard.py",
                "skills/paper-spine-audit/scripts/latex_guard.py",
            ],
            "scripts/revision_audit.py": [
                "skills/paper-spine-audit/scripts/revision_audit.py",
            ],
        }
        for source, targets in copies.items():
            source_text = read(source)
            for target in targets:
                self.assertEqual(read(target), source_text, target)

    def test_readme_documents_suite_modes_and_install_paths(self) -> None:
        text = read("README.md")
        required_fragments = [
            ".claude-plugin",
            "paper-spine-intake",
            "paper-spine-research",
            "paper-spine-rewrite",
            "paper-spine-build",
            "paper-spine-latex",
            "paper-spine-audit",
            "flash",
            "pro",
            "journal",
            "conference",
            "report/review",
            "competition",
            "English",
            "Chinese",
            "Build From Materials",
            "word_guard.py",
            "translation_package",
            "main.tex",
            "Restart Codex",
            "/plugin marketplace add",
            "/plugin install paper-spine",
            "artifact_check.py paper_rewriting_output --markdown --write",
            "codex/paper-spine",
            "/paperspine",
        ]
        missing = [fragment for fragment in required_fragments if fragment not in text]
        self.assertEqual(missing, [])

    def test_paperspine_command_is_primary_auto_intake_entry(self) -> None:
        text = read("commands/paperspine.md")
        self.assertIn("description: Start PaperSpine", text)
        self.assertIn("launch the PaperSpine intake UI automatically", text)
        self.assertIn("paper_spine_config.json", text)
        self.assertIn("launch_paperspine_ui.ps1", text)
        self.assertIn("paper-spine` orchestrator", text)
        legacy = read("commands/paperspine-ui.md")
        self.assertIn("Prefer `/paperspine`", legacy)

    def test_claude_plugin_manifest_uses_flat_suite_skills(self) -> None:
        plugin = json.loads(read(".claude-plugin/plugin.json"))
        marketplace = json.loads(read(".claude-plugin/marketplace.json"))
        self.assertEqual(plugin["name"], "paper-spine")
        self.assertEqual(marketplace["plugins"][0]["name"], "paper-spine")
        skills = marketplace["plugins"][0]["skills"]
        expected = [f"./skills/{name}" for name in SUITE_SKILLS]
        self.assertEqual(skills, expected)
        self.assertTrue((ROOT / ".claude-plugin" / "plugin.json").exists())
        for skill_path in skills:
            self.assertTrue((ROOT / skill_path.removeprefix("./") / "SKILL.md").exists())
    def test_codex_release_layout_uses_single_official_skill_folder(self) -> None:
        self.assertTrue((ROOT / "codex" / "paper-spine" / "SKILL.md").exists())
        self.assertTrue((ROOT / "codex" / "paper-spine" / "scripts" / "intake_wizard.py").exists())
        self.assertTrue((ROOT / "codex" / "paper-spine" / "references" / "writing-rationale-matrix.md").exists())
        self.assertFalse((ROOT / "codex" / "paper-spine-research" / "SKILL.md").exists())
        self.assertFalse((ROOT / "codex" / "PaperSpine" / "SKILL.md").exists())
        self.assertFalse((ROOT / "codex" / "SKILL.md").exists())

    def test_sync_script_exports_expected_layouts_to_temp_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "desktop" / "PaperSpine" / "codex").mkdir(parents=True)
            (base / "desktop" / "PaperSpine" / "claude-code").mkdir(parents=True)
            (base / "codex" / "skills" / "PaperSpineV2").mkdir(parents=True)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/sync_local_installs.py",
                    "--clean-legacy",
                    "--desktop-root",
                    str(base / "desktop" / "PaperSpine"),
                    "--codex-skills-dir",
                    str(base / "codex" / "skills"),
                    "--claude-skills-dir",
                    str(base / "claude" / "skills"),
                    "--claude-commands-dir",
                    str(base / "claude" / "commands"),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((base / "desktop" / "PaperSpine" / "codex" / "paper-spine" / "SKILL.md").exists())
            self.assertFalse((base / "desktop" / "PaperSpine" / "codex" / "paper-spine-research" / "SKILL.md").exists())
            self.assertTrue((base / "desktop" / "PaperSpine" / "claude-code" / ".claude-plugin" / "plugin.json").exists())
            self.assertTrue((base / "desktop" / "PaperSpine" / "claude-code" / "commands" / "paperspine.md").exists())
            self.assertTrue((base / "desktop" / "PaperSpine" / "claude-code" / "commands" / "paperspine-ui.md").exists())
            self.assertTrue((base / "desktop" / "PaperSpine" / "claude-code" / "skills" / "paper-spine" / "SKILL.md").exists())
            self.assertFalse((base / "desktop" / "PaperSpine" / "SKILL.md").exists())
            self.assertFalse((base / "codex" / "skills" / "PaperSpine").exists())
            self.assertTrue((base / "codex" / "skills" / "paper-spine" / "SKILL.md").exists())
            self.assertFalse((base / "codex" / "skills" / "paper-spine-research" / "SKILL.md").exists())
            self.assertTrue((base / "claude" / "skills" / "paper-spine" / "SKILL.md").exists())
            self.assertTrue((base / "claude" / "commands" / "paperspine.md").exists())
            self.assertTrue((base / "claude" / "commands" / "paperspine-ui.md").exists())
            self.assertTrue((base / "desktop" / "PaperSpine" / "codex").exists())
            self.assertTrue((base / "desktop" / "PaperSpine" / "claude-code").exists())
            self.assertFalse((base / "codex" / "skills" / "PaperSpineV2").exists())
            self.assertFalse((base / "claude" / "skills" / "PaperSpineV2" / "skills" / "paper-spine" / "SKILL.md").exists())

    def test_sync_script_does_not_delete_source_when_desktop_root_is_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/sync_local_installs.py",
                    "--desktop-root",
                    str(ROOT),
                    "--codex-skills-dir",
                    str(base / "codex" / "skills"),
                    "--claude-skills-dir",
                    str(base / "claude" / "skills"),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertTrue((ROOT / "README.md").exists())
            self.assertTrue((base / "codex" / "skills" / "paper-spine" / "SKILL.md").exists())
            self.assertTrue((base / "claude" / "skills" / "paper-spine" / "SKILL.md").exists())

    def test_gitignore_blocks_user_and_generated_artifacts(self) -> None:
        text = read(".gitignore")
        required_fragments = [
            "paper_rewriting_output/",
            "tmp_*_artifacts/",
            "*.aux",
            "*.log",
            "*.docx",
            "*.pdf",
        ]
        missing = [fragment for fragment in required_fragments if fragment not in text]
        self.assertEqual(missing, [])

    def test_plugin_root_has_no_top_level_skill_to_avoid_duplicate_discovery(self) -> None:
        self.assertFalse((ROOT / "SKILL.md").exists())
        self.assertTrue((ROOT / ".claude-plugin" / "plugin.json").exists())
        self.assertTrue((ROOT / "skills" / "paper-spine" / "SKILL.md").exists())

    def test_suite_install_layout_can_be_copied_to_temp_skills_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "skills"
            dest.mkdir()
            for skill in SUITE_SKILLS:
                shutil.copytree(ROOT / "skills" / skill, dest / skill)
            missing = [
                skill
                for skill in SUITE_SKILLS
                if not (dest / skill / "SKILL.md").exists()
            ]
            self.assertEqual(missing, [])
            self.assertTrue((dest / "paper-spine-intake" / "scripts" / "intake_wizard.py").exists())
            self.assertTrue((dest / "paper-spine-research" / "references" / "scenario-journal.md").exists())

    def test_plugin_layout_can_be_copied_to_temp_project_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "paper-spine"
            dest.mkdir()
            for name in ["README.md", "LICENSE", ".gitignore"]:
                shutil.copy2(ROOT / name, dest / name)
            shutil.copytree(ROOT / ".claude-plugin", dest / ".claude-plugin")
            shutil.copytree(ROOT / "references", dest / "references")
            shutil.copytree(ROOT / "skills", dest / "skills")
            shutil.copytree(ROOT / "scripts", dest / "scripts")
            self.assertFalse((dest / "SKILL.md").exists())
            self.assertTrue((dest / ".claude-plugin" / "plugin.json").exists())
            self.assertTrue((dest / "references" / "task-genre-research.md").exists())
            self.assertTrue((dest / "skills" / "paper-spine" / "SKILL.md").exists())
            self.assertTrue((dest / "scripts" / "intake_wizard.py").exists())
            self.assertTrue((dest / "scripts" / "launch_paperspine_ui.ps1").exists())


if __name__ == "__main__":
    unittest.main()




