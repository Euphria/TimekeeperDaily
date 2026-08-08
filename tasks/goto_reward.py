"""
建立一条从homepage到奖励界面的路径, 领奖后并返回homepage
路径中包含一系列按钮的点击顺序。
"""

from core.button_click import (
    click_return,
    click_home
)
from core.logger import logger
from core.config import config
from core.actions import find_and_click

def get_task_reward() -> bool:
    """从主页进入奖励页面, 领取奖励后返回主页。"""
    logger.info("开始从主页进入奖励页面")
    config_find_reward = config["tasks"]["goto_reward"]["task"]

    # 进入奖励页面
    if not find_and_click(
        target_path=config_find_reward["PATH"],
        threshold=config_find_reward["THRESHOLD"],
        timeout=config_find_reward["TIMEOUT"],
        interval=config_find_reward["INTERVAL"]
    ):
        logger.error("未找到奖励按钮，无法进入奖励页面")
        print("未找到奖励按钮，无法进入奖励页面")
        return False

    # 全部领取奖励
    config_claim_all = config_find_reward["claim_all"]
    if not find_and_click(
        target_path=config_claim_all["PATH"],
        threshold=config_claim_all["THRESHOLD"],
        timeout=config_claim_all["TIMEOUT"],
        interval=config_claim_all["INTERVAL"]
    ):
        logger.error("未找到领取奖励按钮，无法领取奖励")
        print("未找到领取奖励按钮，无法领取奖励")
        return False

    # 点击obtained并退回到homepage
    config_obtained = config_find_reward["obtained"]
    if not find_and_click(
        target_path=config_obtained["PATH"],
        threshold=config_obtained["THRESHOLD"],
        timeout=config_obtained["TIMEOUT"],
        interval=config_obtained["INTERVAL"]
    ):
        logger.error("未找到获得物品按钮，无法退回到主页")
        print("未找到获得物品按钮，无法退回到主页")
        return False

    if not click_return():
        logger.error("未找到返回按钮，无法返回主页")
        print("未找到返回按钮，无法返回主页")
        return False

    logger.info("成功领取奖励并返回主页")
    return True

if __name__ == "__main__":
    # 测试get_task_reward函数
    from core.window import find_open_window
    print("开始测试get_task_reward函数")
    find_open_window(title_keywords=["MuMu模拟器"])
    get_task_reward()