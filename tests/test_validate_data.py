"""校验功能的单元测试"""

import shutil
from typing import TYPE_CHECKING

from cu_chinese_wiki_translations.validate_data import main, validate_file

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_returns_true_for_valid_yaml(data_dir: Path) -> None:
    """对于合法的yaml文件应该返回True"""
    yaml_path = data_dir / "valid.yaml"

    assert validate_file(yaml_path) is True


def test_returns_false_for_invalid_yaml(data_dir: Path) -> None:
    """对于不合法的yaml文件应该返回False"""
    yaml_path = data_dir / "invalid.yaml"

    assert validate_file(yaml_path) is False


def test_main_returns_zero_when_all_yaml_files_are_valid(
    tmp_path: Path,
    data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """当所有yaml都合法时入口函数应返回0"""
    shutil.copy(data_dir / "valid.yaml", tmp_path / "valid.yaml")
    monkeypatch.chdir(tmp_path)
    assert main() == 0


def test_main_returns_one_when_any_yaml_file_is_invalid(
    tmp_path: Path,
    data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """当任意yaml非法时入口函数应返回1"""
    shutil.copy(data_dir / "invalid.yaml", tmp_path / "invalid.yaml")
    shutil.copy(data_dir / "valid.yaml", tmp_path / "valid.yaml")
    monkeypatch.chdir(tmp_path)
    assert main() == 1
