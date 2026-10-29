"""合并功能的单元测试"""

import json
from copy import deepcopy
from pathlib import Path

import pytest

from cu_chinese_wiki_translations import merge_data as merge_data_module
from cu_chinese_wiki_translations.merge_data import (
    DEMO_JSON,
    OUTPUT_JSON,
    RAW_YAML,
    VENDOR_JSON,
    added_key_paths,
    append_string,
    load_json,
    load_yaml,
    main,
    merge_data,
    parse_args,
    select_vendor,
)


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


def test_parse_args_uses_default_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """未传参数时parse_args应使用默认路径"""
    monkeypatch.setattr("sys.argv", ["merge-trans"])
    monkeypatch.chdir(tmp_path)
    VENDOR_JSON.parent.mkdir(parents=True)
    VENDOR_JSON.touch()

    args = parse_args()

    assert args.vendor == VENDOR_JSON
    assert args.raw == RAW_YAML
    assert args.output == OUTPUT_JSON


@pytest.mark.parametrize("release", [True, False])
def test_default_vendor_selection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    *,
    release: bool,
) -> None:
    """默认选择只根据 release 是否存在, 回退时有提示"""
    monkeypatch.chdir(tmp_path)
    DEMO_JSON.parent.mkdir(parents=True)
    DEMO_JSON.touch()
    if release:
        VENDOR_JSON.parent.mkdir(parents=True)
        VENDOR_JSON.touch()
    assert select_vendor(None) == (VENDOR_JSON if release else DEMO_JSON)
    assert ("回退" in capsys.readouterr().out) is not release
    assert select_vendor(Path("missing-explicit.json")) == Path("missing-explicit.json")


def test_missing_default_vendor_reports_both_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
) -> None:
    """缺少两个默认文件时提供可操作的错误"""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["merge-trans"])
    with pytest.raises(SystemExit, match="2"):
        parse_args()
    error = capsys.readouterr().err
    assert str(VENDOR_JSON) in error
    assert str(DEMO_JSON) in error


def test_invalid_release_does_not_fall_back(
    tmp_path: Path, data_dir: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Release 存在但损坏时必须报错, 不能改用有效 demo"""
    monkeypatch.chdir(tmp_path)
    VENDOR_JSON.parent.mkdir(parents=True)
    VENDOR_JSON.write_text("not json", encoding="utf-8")
    DEMO_JSON.parent.mkdir(parents=True)
    DEMO_JSON.write_text(
        (data_dir / "vendor.json").read_text(encoding="utf-8"), encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["merge-trans", "-r", str(data_dir / "raw.yaml")])
    with pytest.raises(json.JSONDecodeError):
        main()
    assert not OUTPUT_JSON.exists()


def test_added_keys_follow_actual_merge(data_dir: Path) -> None:
    """新增键包含 null、空字典及整个列表; 保留原有类型冲突规则"""
    vendor = load_json(data_dir / "vendor.json")
    raw = load_yaml(data_dir / "raw.yaml")
    raw["main"].update({"new": None, "bandage": {"ignored": "x"}})
    raw["extra"] = {
        "nested": {"value": "x"},
        "list": [{"not_expanded": "x"}],
        "empty": {},
    }
    merged = merge_data(raw, vendor)
    assert added_key_paths(vendor, merged) == [
        "main.new",
        "extra.nested.value",
        "extra.list",
        "extra.empty",
    ]
    assert merged["main"]["new"] is None
    assert merged["main"]["bandage"] == vendor["main"]["bandage"]
    assert merged["extra"] == raw["extra"]


@pytest.mark.parametrize("verbose", [True, False])
def test_cli_reports_same_inputs_and_added_count(
    tmp_path: Path,
    data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
    *,
    verbose: bool,
) -> None:
    """报告与 stdout 使用同一输入记录; 只有 verbose 列新增键名"""
    vendor_path = tmp_path / "vendor.json"
    vendor = load_json(data_dir / "vendor.json")
    vendor["version"] = "upstream-version"
    vendor_path.write_text(json.dumps(vendor), encoding="utf-8")
    raw_path = tmp_path / "raw.yaml"
    raw = load_yaml(data_dir / "raw.yaml")
    raw["main"]["new_key"] = "extension"
    raw_path.write_text(json.dumps(raw), encoding="utf-8")
    report_path = tmp_path / "build.md"
    output = tmp_path / "output.json"
    argv = [
        "merge-trans",
        "-v",
        str(vendor_path),
        "-r",
        str(raw_path),
        "-o",
        str(output),
        "--build-info",
        str(report_path),
    ]
    monkeypatch.setattr("sys.argv", [*argv, *(["--verbose"] if verbose else [])])
    monkeypatch.setenv("PATH", "")
    main()
    stdout = capsys.readouterr().out
    report = report_path.read_text(encoding="utf-8")
    for value in (
        str(vendor_path),
        str(raw_path),
        "upstream-version",
        "v1.8.3",
        "git unavailable",
        "新增键数量：1",
    ):
        assert value in stdout
        assert value in report
    assert "<code>" not in stdout
    assert "&quot;" not in stdout
    assert "version: upstream-version | HEAD:" in stdout
    assert "new_key" not in report
    assert ("main.new_key" in stdout) is verbose
    assert (
        json.loads(output.read_text(encoding="utf-8"))["main"]["new_key"] == "extension"
    )


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
