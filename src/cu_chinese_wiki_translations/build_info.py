"""记录本次合并所用磁盘输入的来源"""

import json
import subprocess
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence


@dataclass(frozen=True)
class InputInfo:
    """单个输入文件的版本与 Git 状态"""

    role: str
    path: str
    version: str
    repository: str = "git unavailable"
    head: str = "git unavailable"
    state: str = "git unavailable"


def _git(directory: Path, *args: str) -> str:
    """在输入所属目录执行只读 Git 命令"""
    return subprocess.run(  # noqa: S603
        ["git", "--literal-pathspecs", "-C", str(directory), *args],  # noqa: S607
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout


def inspect_input(role: str, path: Path, data: Mapping) -> InputInfo:
    """从已加载的数据及该文件所属仓库收集记录, Git 不可用不阻断合并"""
    version = data.get("version", "缺失")
    if not isinstance(version, str):
        version = json.dumps(version, ensure_ascii=False)
    resolved = path.resolve()
    try:
        repository = _git(resolved.parent, "rev-parse", "--show-toplevel").strip()
        head = _git(resolved.parent, "rev-parse", "HEAD").strip()
        relative = str(resolved.relative_to(repository))
        status = _git(
            Path(repository),
            "status",
            "--porcelain=v1",
            "-z",
            "--untracked-files=all",
            "--ignored",
            "--",
            relative,
        )[:2]
    except OSError, ValueError, subprocess.SubprocessError:
        return InputInfo(role, str(path), version)

    if status in {"??", "!!"}:
        state = "untracked"
    elif not status:
        state = "clean"
    elif status[0] != " " and status[1] != " ":
        state = "both"
    else:
        state = "staged" if status[0] != " " else "unstaged"
    return InputInfo(role, str(path), version, repository, head, state)


def render_build_info(inputs: Sequence[InputInfo], added_count: int) -> str:
    """生成 Actions summary 和 Release 可复用的 Markdown"""
    lines = [
        "## 构建输入",
        "",
        "| 输入 | 路径 | 文件 version | HEAD | 文件状态 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for info in inputs:
        values = (
            info.role,
            info.path,
            info.version,
            info.head,
            info.state,
        )
        cells = [
            "<code>"
            + escape(value)
            .replace("|", "&#124;")
            .replace("\n", "&#10;")
            .replace("\r", "&#13;")
            + "</code>"
            for value in values
        ]
        lines.append("| " + " | ".join(cells) + " |")
    lines.extend(["", f"新增键数量：{added_count}", ""])
    return "\n".join(lines)
