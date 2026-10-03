"""环境自检：Python 版本、依赖、FUYAO_API_KEY 与数据源连通性。"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path


MIN_PYTHON = (3, 7)
MAX_PYTHON = (3, 12)
REQUIRED = ["pandas", "numpy", "matplotlib", "requests"]


def python_ok(version_str: str) -> tuple:
    parts = tuple(int(x) for x in version_str.split(".")[:2])
    if parts < MIN_PYTHON:
        return False, "Python 需要 >= 3.7，当前 %s" % version_str
    if parts > MAX_PYTHON:
        return True, "Python %s 高于已实测上限 3.12，仅作警告，不阻断" % version_str
    return True, "Python %s 支持" % version_str


def check_dependencies() -> list:
    results = []
    for name in REQUIRED:
        try:
            mod = importlib.import_module(name)
            results.append((name, True, getattr(mod, "__version__", "?")))
        except Exception as exc:
            results.append((name, False, str(exc)))
    return results


def resolve_api_key(root: Path, runtime_key: str = "") -> str:
    return (runtime_key or os.environ.get("FUYAO_API_KEY", "")).strip()


def check_token(root: Path, runtime_key: str = "") -> tuple:
    key = resolve_api_key(root, runtime_key)
    if not key:
        return False, "未提供 API Key（可手动提供或使用环境变量 FUYAO_API_KEY）"
    return True, "API Key 已提供（仅本次进程使用）"


def check_network(root: Path, runtime_key: str = "") -> tuple:
    sys.path.insert(0, str(root / "scripts"))
    try:
        from data_client import FuyaoClient

        items = FuyaoClient(api_key=runtime_key or None, skill_action="env_check").search("沪深300", asset_type="fund-otc", limit=1)
        return bool(items), "同花顺金融数据API 连通，样例返回 %d 条" % len(items)
    except Exception as exc:
        return False, "同花顺金融数据API 连通失败：%s" % exc


def main(runtime_key: str = ""):
    root = Path(__file__).resolve().parents[1]
    ok, msg = python_ok(".".join(str(x) for x in sys.version_info[:3]))
    print("[Python] " + msg)
    status = ok
    for name, ok_dep, ver in check_dependencies():
        print("[依赖] %s=%s %s" % (name, ver, "OK" if ok_dep else "MISSING"))
        status = status and ok_dep
    token_ok, token_msg = check_token(root, runtime_key)
    print("[API Key] " + token_msg)
    status = status and token_ok
    if token_ok:
        net_ok, net_msg = check_network(root, runtime_key)
        print("[数据源] " + net_msg)
    else:
        net_ok = False
        print("[数据源] 未提供 Key，已跳过同花顺金融数据API连通性检查")
        print(
            "还没有可用的同花顺金融数据API Key。请登录 https://fuyao.aicubes.cn "
            "→ API Key 管理页签发，然后直接提供给当前对话；也可以使用环境变量 FUYAO_API_KEY。"
            "Key 只在当前进程内使用，不会回显或写入文件、日志、配置。"
        )
    if not (token_ok and net_ok):
        print("\n提示：API Key/网络失败只影响取数，回测脚本仍可检查本地缓存。")
    sys.exit(0 if status else 1)


if __name__ == "__main__":
    main()
