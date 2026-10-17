#!/usr/bin/env python3
"""
verify_handoff.py
Utility script to validate a handoff document:
- Checks if referenced file paths exist on disk.
- Scans for potentially leaked secrets or credentials.
- Validates standard schema sections.
"""

import sys
import os
import re
from pathlib import Path

POTENTIAL_SECRET_PATTERNS = [
    r"(?i)(api[_-]?key|secret|token|password|auth|bearer)\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]{12,}['\"]?",
    r"sk-[A-Za-z0-9]{20,}",
    r"ghp_[A-Za-z0-9]{30,}",
    r"-----BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY-----"
]

def verify_handoff_file(file_path: str):
    p = Path(file_path)
    if not p.is_file():
        print(f"[ERROR] Handoff file not found: {file_path}")
        return False

    content = p.read_text(encoding="utf-8", errors="ignore")
    print(f"[INFO] Analyzing handoff file: {p.resolve()}")

    # 1. Check for sensitive information leaks
    leak_found = False
    for pat in POTENTIAL_SECRET_PATTERNS:
        matches = re.findall(pat, content)
        if matches:
            print(f"[WARNING] Potential unredacted secret detected matching pattern: {pat}")
            leak_found = True

    if not leak_found:
        print("[PASS] No exposed secrets or API keys detected.")

    # 2. Check for referenced backtick file paths
    # Matches strings like `src/app.py` or `tests/test_x.py`
    potential_files = re.findall(r"`([a-zA-Z0-9_\-\./\\]+\.[a-zA-Z0-9]+)`", content)
    missing_files = []
    found_files = []
    
    workspace_root = Path.cwd()
    for rel_path in potential_files:
        # Ignore common technical terms with dots
        if rel_path.lower() in ("package.json", "skill.md", "readme.md", "context.md") or "/" in rel_path or "\\" in rel_path:
            target = workspace_root / rel_path
            if target.exists():
                found_files.append(rel_path)
            else:
                missing_files.append(rel_path)

    print(f"[CHECK] Referenced file touchpoints: {len(found_files)} found, {len(missing_files)} missing on disk.")
    if missing_files:
        for mf in missing_files:
            print(f"  [?] File path not found on disk: {mf}")

    # 3. Check for core sections
    required_sections = ["Objective", "Progress", "Decisions", "Next Steps"]
    missing_sections = []
    for s in required_sections:
        if not re.search(rf"(?i)#{1,3}\s+.*{s}", content):
            missing_sections.append(s)

    if missing_sections:
        print(f"[NOTICE] Recommended sections missing from document: {', '.join(missing_sections)}")
    else:
        print("[PASS] Core handoff sections present.")

    print("[DONE] Verification finished.")
    return True

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else ".handoff/HANDOFF_LATEST.md"
    verify_handoff_file(target)
