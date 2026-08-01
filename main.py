"""项目启动器：按顺序调用 core 和 tasks 中的函数完成日常流程。"""

from core.config import load_config
from core.launch import launch_game, close_game
from core.logger import logger

from tasks.login import login_game

from time import sleep


def main() -> None:
    """
    程序入口函数。

    main.py 只负责串联流程，不直接实现具体操作。
    1. 启动游戏
    2. 登录游戏
    3. 关闭游戏
    """
    config = load_config("config.yaml")
    logger.info("Timekeeper Daily 开始运行")

    # 启动游戏
    if not launch_game(keyword=config["launch"]["launch_keyword"]):
        logger.error("游戏启动失败，终止运行")
        return

    # 登录游戏
    if not login_game(config["tasks"]["login"]):
        logger.error("游戏登录失败，终止运行")
        return

    # 关闭游戏
    sleep(5)  # 等待 10 秒后尝试关闭游戏

    if not close_game(keyword=config["launch"]["close_keyword"]):
        logger.error("游戏关闭失败，终止运行")
        return

    logger.info("游戏已关闭, Timekeeper Daily 运行结束")


if __name__ == "__main__":
    main()
