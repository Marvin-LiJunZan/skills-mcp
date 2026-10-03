"""编码与打包质检：无 BOM UTF-8、无 U+FFFD、ASCII 文件名。"""

from __future__ import annotations

import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".json", ".py", ".txt"}
EXCLUDE_DIRS = {
    ".git",
    ".pytest_cache",
    ".superpowers",
    "__pycache__",
    "data_cache",
    "reports",
}
KEY_FILES = {".env", ".env.example"}


def iter_package_files(root: Path, errors: list):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if path.name in KEY_FILES:
            errors.append("%s：禁止包含 Key 配置文件" % rel)
            continue
        yield path, rel


def check_encoding(root: Path = None) -> list:
    root = Path(root) if root is not None else ROOT
    errors = []
    non_ascii = []
    for path, rel in iter_package_files(root, errors):
        try:
            str(rel).encode("ascii")
        except UnicodeEncodeError:
            non_ascii.append(rel)
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            errors.append("%s：无法读取（%s）" % (rel, exc))
            continue
        if data.startswith(b"\xef\xbb\xbf"):
            errors.append("%s：文件含 BOM" % rel)
        if "\ufffd" in data.decode("utf-8", errors="replace"):
            errors.append("%s：含 Unicode 替换字符 U+FFFD" % rel)
    if non_ascii:
        errors.append("文件名非 ASCII：" + "、".join(str(r) for r in non_ascii))
    return errors


def main():
    errors = check_encoding()
    if errors:
        print("编码质检失败：")
        for error in errors:
            print(" - " + error)
        sys.exit(1)
    print("编码质检通过：源文件无 BOM UTF-8、无 U+FFFD、文件名 ASCII。")


if __name__ == "__main__":
    main()
