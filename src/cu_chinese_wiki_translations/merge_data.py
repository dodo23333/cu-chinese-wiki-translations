"""合并基准翻译和中间文件"""

from __future__ import annotations

import json
from argparse import ArgumentParser, Namespace
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from deepmerge.merger import Merger

from cu_chinese_wiki_translations.validate_data import validate_file

if TYPE_CHECKING:
    from collections.abc import MutableMapping

VENDOR_JSON = Path("vendor/zh-CN.json")
RAW_YAML = Path("wiki-patch.yaml")
OUTPUT_JSON = Path("wiki-translations-official.json")

# 元数据键：不参与正文合并，由 merge_data 单独处理
METADATA_KEYS = {
    "name",
    "version",
    "extend_description",
    "description",
    "version_override",
}

# 值以该前缀开头时，表示「整体替换基准文本」而非追加
REPLACE_TAG = "!R!"


def load_yaml(path: Path) -> dict:
    """加载yaml文件"""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    """加载json文件"""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def strip_replace_tag(value: str) -> str:
    """去掉替换标记，返回实际文本"""
    return value[len(REPLACE_TAG):]


def append_string(config: Merger, path: list, base: str, nxt: str) -> str:
    """合并字符串的规范

    若 nxt 以 !R! 开头，则整体替换 base，不追加。
    """
    if isinstance(nxt, str) and nxt.startswith(REPLACE_TAG):
        return strip_replace_tag(nxt)
    if not base:
        return nxt
    if not nxt:
        return base

    key = str(path[-1]) if path else ""
    return f"{base}\n{nxt}" if key.endswith("dsc") else f"{base}{nxt}"


def cleanup_replace_tags(data: MutableMapping) -> None:
    """清理未被合并流程处理的 !R! 标记

    当补丁中的键在基准文件中不存在时，deepmerge 会直接写入原值，
    不会调用 append_string，此时需要在这里去掉标记。
    """
    for key, value in data.items():
        if isinstance(value, str) and value.startswith(REPLACE_TAG):
            data[key] = strip_replace_tag(value)
        elif isinstance(value, dict):
            cleanup_replace_tags(value)


translation_merger = Merger(
    [
        (dict, ["merge"]),
        (list, ["override"]),
        (str, append_string),
    ],
    ["override"],
    ["use_existing"],
)


def merge_data(raw: dict, vendor: dict) -> MutableMapping:
    """合并两个dict"""
    merged = deepcopy(vendor)
    raw_patch = {key: value for key, value in raw.items() if key not in METADATA_KEYS}

    translation_merger.merge(merged, raw_patch)
    cleanup_replace_tags(merged)

    merged["name"] = raw["name"] + raw["version"]

    # description：优先整体替换，其次追加 extend_description
    if raw.get("description"):
        merged["description"] = raw["description"]
    elif raw.get("extend_description"):
        merged["description"] = merged.get("description", "") + "\n" + raw["extend_description"]

    # version 字段覆盖
    if raw.get("version_override"):
        merged["version"] = str(raw["version_override"])

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

    validate_file(args.raw)
    validate_file(args.vendor)

    raw_data = load_yaml(args.raw)
    vendor_data = load_json(args.vendor)

    merged_data = merge_data(raw_data, vendor_data)

    with args.output.open("w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":  # pragma: no cover
    main()
