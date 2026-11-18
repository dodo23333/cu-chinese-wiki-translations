"""合并基准翻译和中间文件"""

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
METADATA_KEYS = {"name", "version", "extend_description", "description"}


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


def _reject_lists(patch: dict, parent: str = "") -> None:
    for key, value in patch.items():
        if isinstance(value, dict):
            _reject_lists(value, f"{parent}{key}.")
        elif isinstance(value, list):
            raise ValueError(f"{parent}{key}: 列表须写在 replace: 下")


def _apply_replacements(
    merged: dict, vendor: dict, patch: dict, replacements: object
) -> None:
    if not isinstance(replacements, dict):
        raise ValueError("replace: 必须是分区映射")
    for section, values in replacements.items():
        if not isinstance(values, dict):
            raise ValueError(f"replace.{section}: 必须是条目映射")
        base_section = vendor.get(section)
        patch_section = patch.get(section)
        for key, value in values.items():
            path = f"replace.{section}.{key}"
            if not isinstance(base_section, dict) or key not in base_section:
                raise ValueError(f"{path}: 基准中没有该条目")
            if isinstance(patch_section, dict) and key in patch_section:
                raise ValueError(f"{path}: 与普通分区 {section}.{key} 重复")
            base_value = base_section[key]
            if not (
                (isinstance(base_value, str) and isinstance(value, str))
                or (
                    isinstance(base_value, list)
                    and isinstance(value, list)
                    and all(isinstance(item, str) for item in value)
                )
            ):
                raise ValueError(f"{path}: 替换值类型须与基准一致")
            merged[section][key] = value


translation_merger = Merger(
    [
        (dict, ["merge"]),
        (str, append_string),
    ],
    ["override"],
    ["use_existing"],
)


def merge_data(raw: dict, vendor: dict) -> MutableMapping:
    """合并两个dict"""
    raw_patch = {
        key: value
        for key, value in raw.items()
        if key not in METADATA_KEYS and key != "replace"
    }
    _reject_lists(raw_patch)

    merged = deepcopy(vendor)
    translation_merger.merge(merged, raw_patch)
    _apply_replacements(merged, vendor, raw_patch, raw.get("replace", {}))

    merged["name"] = raw["name"] + raw["version"]

    # version：去掉补丁版本号的前缀 v，作为产物的 version 字段
    merged["version"] = str(raw["version"]).removeprefix("v")

    # description：优先整体替换，其次追加 extend_description
    if raw.get("description"):
        merged["description"] = raw["description"]
    elif raw.get("extend_description"):
        merged["description"] = merged.get("description", "") + "\n" + raw["extend_description"]

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
