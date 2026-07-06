"""合并功能的单元测试"""

import json
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

from cu_chinese_wiki_translations import merge_data as merge_data_module
from cu_chinese_wiki_translations.merge_data import (
    OUTPUT_JSON,
    RAW_YAML,
    VENDOR_JSON,
    append_string,
    load_json,
    load_yaml,
    main,
    merge_data,
    parse_args,
)

if TYPE_CHECKING:
    import pytest


def test_load_json_reads_mapping(data_dir: Path) -> None:
    """load_json应正常读取json文件并返回dict"""
    json_path = data_dir / "vendor.json"

    assert load_json(json_path) == {
        "name": "简体中文",
        "description": "官方简介",
        "main": {"bandage": "绷带", "bandagedsc": "带有敷料的绷带"},
    }


def test_load_yaml_reads_mapping(data_dir: Path) -> None:
    """load_yaml应正常读取yaml文件并返回dict"""
    yaml_path = data_dir / "raw.yaml"

    assert load_yaml(yaml_path) == {
        "name": "维基中文",
        "version": "v1.8.3",
        "main": {"bandagedsc": "可治疗伤势"},
        "extend_description": "补充简介",
    }


def test_append_string_returns_other_side_when_one_side_is_empty() -> None:
    """字符串合并时空字符串不应产生额外内容"""
    merger = merge_data_module.translation_merger

    assert append_string(merger, ["name"], "", "附加") == "附加"
    assert append_string(merger, ["name"], "官方", "") == "官方"


def test_append_string_joins_description_fields_with_newline() -> None:
    """以dsc结尾的字段应换行"""
    merger = merge_data_module.translation_merger

    assert (
        append_string(merger, ["main", "bandagedsc"], "官方描述", "附加描述")
        == "官方描述\n附加描述"
    )


def test_append_string_concatenates_non_description_fields() -> None:
    """非dsc字段应直接拼接字符串"""
    merger = merge_data_module.translation_merger

    assert append_string(merger, ["name"], "官方", "附加") == "官方附加"


def test_merge_data_merges_raw_patch_over_vendor_without_changing(
    data_dir: Path,
) -> None:
    """merge_data应按翻译规则合并, 且不修改原始vendor"""
    vendor = load_json(data_dir / "vendor.json")
    raw = load_yaml(data_dir / "raw.yaml")
    original_vendor = deepcopy(vendor)

    assert merge_data(raw, vendor) == {
        "name": "维基中文v1.8.3",
        "description": "官方简介\n补充简介",
        "main": {
            "bandage": "绷带",
            "bandagedsc": "带有敷料的绷带\n可治疗伤势",
        },
    }
    assert vendor == original_vendor


def test_merge_data_ignores_empty_raw_values(data_dir: Path) -> None:
    """raw中留空的值不应覆盖vendor中的已有翻译"""
    vendor = load_json(data_dir / "vendor.json")
    raw = {
        "name": "维基中文",
        "version": "v1.8.3",
        "extend_description": "补充简介",
        "main": {"bandagedsc": None},
    }

    merged = merge_data(raw, vendor)

    assert merged["main"]["bandagedsc"] == "带有敷料的绷带"


def test_parse_args_uses_default_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    """未传参数时parse_args应使用默认路径"""
    monkeypatch.setattr("sys.argv", ["merge-trans"])

    args = parse_args()

    assert args.vendor == VENDOR_JSON
    assert args.raw == RAW_YAML
    assert args.output == OUTPUT_JSON


def test_parse_args_accepts_custom_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    """传入命令行参数时parse_args应使用自定义路径"""
    monkeypatch.setattr(
        "sys.argv",
        [
            "merge-trans",
            "--vendor",
            "custom-vendor.json",
            "--raw",
            "custom-raw.yaml",
            "--output",
            "custom-output.json",
        ],
    )

    args = parse_args()

    assert args.vendor == Path("custom-vendor.json")
    assert args.raw == Path("custom-raw.yaml")
    assert args.output == Path("custom-output.json")


def test_main_writes_merged_json(
    tmp_path: Path,
    data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """main应读取输入文件并写出合并后的json"""
    vendor_path = data_dir / "vendor.json"
    raw_path = data_dir / "raw.yaml"
    output_path = tmp_path / "merged.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "merge-trans",
            "--vendor",
            str(vendor_path),
            "--raw",
            str(raw_path),
            "--output",
            str(output_path),
        ],
    )

    main()

    assert json.loads(output_path.read_text(encoding="utf-8")) == {
        "name": "维基中文v1.8.3",
        "description": "官方简介\n补充简介",
        "main": {
            "bandage": "绷带",
            "bandagedsc": "带有敷料的绷带\n可治疗伤势",
        },
    }
