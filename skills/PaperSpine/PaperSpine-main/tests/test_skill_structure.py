from __future__ import annotations

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


class SkillStructureTests(unittest.TestCase):
    def test_required_project_files_exist(self) -> None:
        required = [
            "README.md",
            "LICENSE",
            ".gitignore",
            ".claude-plugin/plugin.json",
            ".claude-plugin/marketplace.json",
            "agents/openai.yaml",
            "references/task-genre-research.md",
            "references/version-requirements.md",
            "scripts/latex_guard.py",
            "scripts/revision_audit.py",
            "scripts/style_metrics.py",
            "scripts/intake_wizard.py",
            "scripts/material_inventory.py",
            "scripts/artifact_check.py",
            "scripts/word_guard.py",
            "scripts/sync_local_installs.py",
            "codex/paper-spine/SKILL.md",
        ]
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual(missing, [])

    def test_root_skill_is_absent_to_avoid_duplicate_codex_discovery(self) -> None:
        self.assertFalse((ROOT / "SKILL.md").exists())

    def test_suite_skills_exist(self) -> None:
        missing = [
            name
            for name in SUITE_SKILLS
            if not (ROOT / "skills" / name / "SKILL.md").exists()
        ]
        self.assertEqual(missing, [])

    def test_suite_support_files_exist(self) -> None:
        required = [
            "skills/paper-spine-intake/scripts/intake_wizard.py",
            "skills/paper-spine/scripts/intake_wizard.py",
            "skills/paper-spine/scripts/material_inventory.py",
            "skills/paper-spine/scripts/artifact_check.py",
            "skills/paper-spine-build/scripts/material_inventory.py",
            "skills/paper-spine-audit/scripts/artifact_check.py",
            "skills/paper-spine-latex/scripts/word_guard.py",
            "skills/paper-spine-audit/scripts/word_guard.py",
            "skills/paper-spine-research/references/flash-pro-research.md",
            "skills/paper-spine-research/references/scenario-journal.md",
            "skills/paper-spine-research/references/scenario-conference.md",
            "skills/paper-spine-research/references/scenario-report-review.md",
            "skills/paper-spine-research/references/scenario-competition.md",
            "skills/paper-spine-build/references/build-from-materials.md",
            "skills/paper-spine-intake/references/interactive-intake.md",
            "skills/paper-spine/references/writing-rationale-matrix.md",
            "skills/paper-spine-audit/references/translation-package.md",
        ]
        missing = [path for path in required if not (ROOT / path).exists()]
        self.assertEqual(missing, [])

    def test_no_temporary_artifact_directories(self) -> None:
        tmp_dirs = [path.name for path in ROOT.glob("tmp_*_artifacts") if path.is_dir()]
        self.assertEqual(tmp_dirs, [])

    def test_no_obvious_local_private_paths_in_reusable_files(self) -> None:
        reusable_suffixes = {".md", ".py", ".yaml", ".yml", ".txt", ".json"}
        blocked_fragments = [
            "C:" + "\\Users\\",
            "/Users/",
            "file:" + "///",
            "Bio" + "informatics",
            "M:" + "\\" + "R" + "BP" + "\\",
            "paper" + "_v",
            "oup-" + "authoring",
        ]
        offenders: list[str] = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in reusable_suffixes:
                continue
            if path.name == "test_skill_structure.py":
                continue
            if ".git" in path.parts:
                continue
            if "paper_rewriting_output" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for fragment in blocked_fragments:
                if fragment in text:
                    offenders.append(str(path.relative_to(ROOT)))
                    break
        self.assertEqual(offenders, [])

    def test_skill_metadata_files_have_no_utf8_bom(self) -> None:
        files = [ROOT / "codex" / "paper-spine" / "SKILL.md"] + [
            ROOT / "skills" / name / "SKILL.md" for name in SUITE_SKILLS
        ]
        offenders = []
        for path in files:
            data = path.read_bytes()
            if data.startswith(b"\xef\xbb\xbf"):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])
    def test_frontmatter_description_is_portable(self) -> None:
        skill_files = [ROOT / "skills" / name / "SKILL.md" for name in SUITE_SKILLS]
        offenders: list[str] = []
        for path in skill_files:
            text = path.read_text(encoding="utf-8")
            lines = text.splitlines()
            description = next(line for line in lines if line.startswith("description: "))
            value = description.removeprefix("description: ").strip()
            if len(value) > 200:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()


