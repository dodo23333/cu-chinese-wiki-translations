"""验证yaml文件是否合法"""

import logging
import sys
from pathlib import Path

from rich.logging import RichHandler
from yaml import Node, SafeLoader, ScalarNode, YAMLError, load
from yaml.constructor import ConstructorError

DATA_DIR = Path()
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])
logger = logging.getLogger(__name__)


class ReplaceText(str):
    """用来覆盖基准翻译的字符串。"""


class PatchLoader(SafeLoader):
    """支持自定义标签的yaml加载器。"""


def _construct_replace_text(loader: PatchLoader, node: Node) -> ReplaceText:
    if not isinstance(node, ScalarNode):
        raise ConstructorError(None, None, "!replace 只接受字符串", node.start_mark)
    return ReplaceText(loader.construct_scalar(node))


PatchLoader.add_constructor("!replace", _construct_replace_text)


def load_yaml(path: Path) -> dict:
    """加载 YAML 文件。"""
    with path.open("r", encoding="utf-8") as f:
        return load(f, Loader=PatchLoader)


def validate_file(path: Path) -> bool:
    """验证单个yaml文件"""
    try:
        load_yaml(path)
    except YAMLError:
        logger.error("%s is not a valid YAML file", path, exc_info=False)
        return False
    return True


def main() -> int:
    """验证根目录下所有yaml文件"""
    failed_paths = [
        path for path in DATA_DIR.rglob("*.yaml") if not validate_file(path)
    ]

    if not failed_paths:
        logger.info("All YAML files are valid")
        return 0
    return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
