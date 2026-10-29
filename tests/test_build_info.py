"""构建输入记录测试"""

import subprocess
from typing import TYPE_CHECKING

import pytest

from cu_chinese_wiki_translations.build_info import (
    InputInfo,
    inspect_input,
    render_build_info,
)

if TYPE_CHECKING:
    from pathlib import Path


def git(directory: Path, *args: str) -> str:
    """操作隔离的测试仓库"""
    return subprocess.run(  # noqa: S603
        ["git", "-C", str(directory), *args],  # noqa: S607
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def init_repo(directory: Path) -> Path:
    """建立带提交的测试仓库"""
    directory.mkdir(parents=True, exist_ok=True)
    git(directory, "init")
    git(directory, "config", "user.email", "test@example.invalid")
    git(directory, "config", "user.name", "Test")
    path = directory / "input.json"
    path.write_text("original", encoding="utf-8")
    git(directory, "add", "input.json")
    git(directory, "-c", "commit.gpgsign=false", "commit", "-m", "fixture")
    return path


@pytest.mark.parametrize("state", ["clean", "staged", "unstaged", "both", "untracked"])
def test_input_git_state_is_file_scoped(tmp_path: Path, state: str) -> None:
    """仅记录输入文件状态, 暂存与工作区修改可同时存在"""
    path = init_repo(tmp_path)
    (tmp_path / "unrelated.txt").write_text("unrelated", encoding="utf-8")
    if state == "untracked":
        path = tmp_path / "new.json"
        path.write_text("new", encoding="utf-8")
    elif state != "clean":
        path.write_text("changed", encoding="utf-8")
        if state in {"staged", "both"}:
            git(tmp_path, "add", "input.json")
        if state == "both":
            path.write_text("changed again", encoding="utf-8")
    info = inspect_input("vendor", path, {"version": "v1"})
    assert info.state == state
    assert info.head == git(tmp_path, "rev-parse", "HEAD")
    assert info.repository == str(tmp_path)
    assert info.version == "v1"


def test_input_uses_nearest_repository(tmp_path: Path) -> None:
    """嵌套仓库的 SHA 与文件状态属于内层仓库"""
    init_repo(tmp_path)
    nested = tmp_path / "vendor"
    path = init_repo(nested)
    path.write_text("nested edit", encoding="utf-8")
    info = inspect_input("vendor", path, {})
    assert info.repository == str(nested)
    assert info.head == git(nested, "rev-parse", "HEAD")
    assert info.state == "unstaged"
    assert info.version == "缺失"


def test_non_repository_and_missing_git_are_nonfatal(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """普通目录和未安装 Git 的环境仍提供输入路径与版本"""
    path = tmp_path / "input.json"
    path.touch()
    assert inspect_input("raw", path, {}).state == "git unavailable"
    monkeypatch.setenv("PATH", "")
    assert inspect_input("raw", path, {"version": 1}).version == "1"


def test_report_escapes_markdown_cells() -> None:
    """路径和版本内容不能拆开表格或注入 HTML"""
    report = render_build_info([InputInfo("raw", "a|b\n<c>", "`|x")], 0)
    assert "a&#124;b&#10;&lt;c&gt;" in report
    assert "`&#124;x" in report
    assert "新增键数量：0" in report
