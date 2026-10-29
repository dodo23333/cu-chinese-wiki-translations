"""合并基准翻译和中间文件"""

import json
from argparse import ArgumentParser, Namespace
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from deepmerge.merger import Merger

from cu_chinese_wiki_translations.build_info import inspect_input, render_build_info
from cu_chinese_wiki_translations.validate_data import validate_file

if TYPE_CHECKING:
    from collections.abc import MutableMapping

VENDOR_JSON = Path("vendor/release/zh-CN.json")
DEMO_JSON = Path("vendor/demo/zh-CN.json")
RAW_YAML = Path("维基中文中间文件.yaml")
OUTPUT_JSON = Path("wiki-translations-official.json")
METADATA_KEYS = {"name", "version", "extend_description"}


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
    ["use_existing"],
)


def merge_data(raw: dict, vendor: dict) -> MutableMapping:
    """合并两个dict"""
    merged = deepcopy(vendor)
    raw_patch = {key: value for key, value in raw.items() if key not in METADATA_KEYS}

    translation_merger.merge(merged, raw_patch)
    merged["name"] = raw["name"] + raw["version"]
    merged["description"] = merged["description"] + "\n" + raw["extend_description"]
    return merged


def added_key_paths(vendor: dict, merged: dict) -> list[str]:
    """统计合并后新增的末级字典键路径, 不展开列表或统计元数据"""

    def visit(base: dict, result: dict, prefix: tuple = ()) -> list[str]:
        paths = []
        for key, value in result.items():
            if not prefix and key in METADATA_KEYS:
                continue
            path = (*prefix, str(key))
            if isinstance(value, dict) and value:
                previous = base.get(key, {})
                paths.extend(
                    visit(previous if isinstance(previous, dict) else {}, value, path),
                )
            elif key not in base:
                paths.append(".".join(path))
        return paths

    return visit(vendor, merged)


def select_vendor(explicit: Path | None) -> Path:
    """显式输入优先, 仅在 release 不存在时回退 demo"""
    if explicit is not None:
        return explicit
    for candidate in (VENDOR_JSON, DEMO_JSON):
        try:
            candidate.stat()
        except FileNotFoundError:
            continue
        if candidate == DEMO_JSON:
            print(f"{VENDOR_JSON} 不存在，回退使用 {DEMO_JSON}")  # noqa: T201
        return candidate
    message = f"找不到基准翻译：{VENDOR_JSON} 或 {DEMO_JSON}；可用 -v 指定文件"
    raise FileNotFoundError(message)


def parse_args() -> Namespace:
    """解析命令行参数"""
    parser = ArgumentParser(description="合并基准翻译和wiki汉化组补丁")

    parser.add_argument(
        "-v",
        "--vendor",
        type=Path,
        help=f"基准翻译，默认优先 {VENDOR_JSON}，不存在则回退 {DEMO_JSON}",
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

    parser.add_argument("--verbose", action="store_true", help="列出全部新增键路径")
    parser.add_argument(
        "--build-info", type=Path, help="将本次输入记录写入 Markdown 文件",
    )
    args = parser.parse_args()
    try:
        args.vendor = select_vendor(args.vendor)
    except FileNotFoundError as error:
        parser.error(str(error))
    return args


def main() -> None:
    """合并翻译"""
    args = parse_args()

    validate_file(args.raw)
    validate_file(args.vendor)

    raw_data = load_yaml(args.raw)
    vendor_data = load_json(args.vendor)
    inputs = [
        inspect_input("vendor", args.vendor, vendor_data),
        inspect_input("raw", args.raw, raw_data),
    ]

    merged_data = merge_data(raw_data, vendor_data)
    added = added_key_paths(vendor_data, merged_data)
    for info in inputs:
        print(  # noqa: T201
            f"{info.role}: {info.path} | version: {info.version}"
            f" | HEAD: {info.head} | state: {info.state}",
        )
    print(f"新增键数量：{len(added)}")  # noqa: T201
    if args.verbose:
        for path in added:
            print(f"新增键：{path}")  # noqa: T201

    with args.output.open("w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    if args.build_info is not None:
        args.build_info.write_text(
            render_build_info(inputs, len(added)), encoding="utf-8",
        )


if __name__ == "__main__":  # pragma: no cover
    main()
