"""合并基准翻译和中间文件"""

import json
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from deepmerge import Merger

if TYPE_CHECKING:
    from collections.abc import MutableMapping

VENDOR_JSON = Path("vendor/zh-CN.json")
RAW_YAML = Path("维基中文中间文件.yaml")
OUTPUT_JSON = Path("维基简中.json")


def load_yaml(path: Path) -> dict:
    """加载yaml文件"""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    """加载json文件"""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def append_string(config: Merger, path: list, base: str, nxt: str) -> str:
    """合并字符串的规范"""
    if not base:
        return nxt
    if not nxt:
        return base

    key = str(path[-1]) if path else ""
    return f"{base}\n{nxt}" if key.endswith(".dsc") else f"{base}{nxt}"


translation_merger = Merger(
    [
        (dict, ["merge"]),
        (list, ["override"]),
        (str, append_string),
    ],
    ["override"],
    ["override"],
)


def merge_data(raw: dict, vendor: dict) -> MutableMapping:
    """合并两个dict"""
    merged = deepcopy(vendor)
    translation_merger.merge(merged, raw)
    return merged


def main() -> None:
    """合并翻译"""
    raw_data = load_yaml(RAW_YAML)
    vendor_data = load_json(VENDOR_JSON)

    merged_data = merge_data(raw_data, vendor_data)

    with OUTPUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
