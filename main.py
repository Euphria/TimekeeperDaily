"""项目启动器：按顺序调用 core 和 tasks 中的函数完成日常流程。"""

# core
from core.logger import logger
from core.config import config
from core.launch import (
    launch_game, 
    close_game
)

from core.button_click import (
    click_role
)

from core.window import (
    is_in_homepage,
)

# tasks
from tasks.login import login_game
from tasks.goto_fight import (
    goto_PA_start, #意志解析
    goto_MA_start, #铸币美学
    goto_TP_start, #尘埃运动
)
from tasks.goto_reward import (
    get_task_reward,
)
from tasks.goto_wilderness import (
    goto_wilderness
)

# other
from time import sleep

def main() -> None:
    """
    程序入口函数。

    main.py 只负责串联流程，不直接实现具体操作。
    1. 启动游戏
    2. 登录游戏
    3. 关闭游戏
    """
    logger.info("Timekeeper Daily 开始运行")

    # 启动游戏
    if not launch_game(keyword=config["core"]["launch"]["launch_keyword"]):
        logger.error("游戏启动失败，终止运行")
        print("游戏启动失败，终止运行")
        return

    # 登录游戏
    if not login_game(config["tasks"]["login"]):
        logger.error("游戏登录失败，终止运行")
        print("游戏登录失败，终止运行")
        return

    while not is_in_homepage():
        logger.info("当前不在游戏主页, 等待用户操作结束, 等待 5 秒后重试")
        sleep(5)

    # 点一下小人加好感
    click_role()

    # 开始前往不休荒原 (稍微有点问题, 先注释掉)
    # if not goto_wilderness():
    #     logger.error("前往不休荒原失败，终止运行")
    #     print("前往不休荒原失败，终止运行")
    #     return

    # 开始清体力：PA -> MA
    if not goto_PA_start():
        logger.error("意志解析任务失败，终止运行")
        print("意志解析任务失败，终止运行")
        return
    if not goto_MA_start():
        logger.error("铸币美学任务失败，终止运行")
        print("铸币美学任务失败，终止运行")
        return

    # 开始领奖励
    if not get_task_reward():
        logger.error("领取奖励任务失败，终止运行")
        print("领取奖励任务失败，终止运行")
        return

    # 关闭游戏
    sleep(5)  # 等待 10 秒后尝试关闭游戏

    # if not close_game(keyword=config["core"]["launch"]["close_keyword"]):
    #     logger.error("游戏关闭失败，终止运行")
    #     return

    print("游戏已关闭, Timekeeper Daily 运行结束")
    logger.info("游戏已关闭, Timekeeper Daily 运行结束")


if __name__ == "__main__":
    main()
