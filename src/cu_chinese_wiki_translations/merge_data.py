"""合并基准翻译和中间文件"""

import json
from argparse import ArgumentParser, Namespace
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from deepmerge import Merger

if TYPE_CHECKING:
    from collections.abc import MutableMapping

VENDOR_JSON = Path("vendor/zh-CN.json")
RAW_YAML = Path("维基中文中间文件.yaml")
OUTPUT_JSON = Path("维基中文_基于官方翻译.json")


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
    return f"{base}\n{nxt}" if key.endswith("dsc") else f"{base}{nxt}"


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
    merged["name"] = raw["name"] + raw["version"]
    merged["description"] = merged["description"] + "\n" + raw["extend_description"]
    return merged


def parse_args() -> Namespace:
    """解析命令行参数"""
    parser = ArgumentParser(description="合并基准翻译和wiki汉化组补丁")

    parser.add_argument(
        "-v",
        "--vendor",
        type=Path,
        default=VENDOR_JSON,
        help=f"基准翻译，默认：{VENDOR_JSON}",
    )

    parser.add_argument(
        "-r",
        "--raw",
        type=Path,
        default=RAW_YAML,
        help=f"wiki汉化组补丁，默认：{RAW_YAML}",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=OUTPUT_JSON,
        help=f"合并后文件，默认：{OUTPUT_JSON}",
    )

    return parser.parse_args()


def main() -> None:
    """合并翻译"""
    args = parse_args()

    raw_data = load_yaml(args.raw)
    vendor_data = load_json(args.vendor)

    merged_data = merge_data(raw_data, vendor_data)

    with args.output.open("w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
