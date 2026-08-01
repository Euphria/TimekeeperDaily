"""日志配置：创建全局 logger，并把每次运行的日志写入 logs 目录。"""

from datetime import datetime
import logging
from pathlib import Path


# 项目根目录: timekeeper-daily/core/logger.py -> timekeeper-daily/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 日志目录。
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# 每次运行创建一个新的日志文件。
RUN_TIME = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"{RUN_TIME}.log"


def create_logger() -> logging.Logger:
    """
    创建项目全局日志记录器。

    日志格式为: 当前时间 [日志等级] 输出内容。
    """
    logger = logging.getLogger("timekeeper_daily")

    # 防止模块被重复导入时重复添加 handler。
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(
        filename=LOG_FILE,
        mode="a",
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


logger = create_logger()
