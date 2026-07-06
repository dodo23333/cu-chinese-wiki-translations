"""验证yaml文件是否合法"""

import logging
import sys
from pathlib import Path

from rich.logging import RichHandler
from yaml import YAMLError, safe_load

DATA_DIR = Path()
logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler()])
logger = logging.getLogger(__name__)


def validate_file(path: Path) -> bool:
    """验证单个yaml文件"""
    try:
        with path.open() as f:
            safe_load(f)
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
