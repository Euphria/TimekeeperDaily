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

def click_claim(config_find_reward):
    """
    点击领取奖励按钮

    1, 按顺序从config["tasks"]["goto_reward"]["task"]["claim"]的path中查找领取按钮
    2, 点击后确认obtained
    
    """
    logger.info("查找并点击领取按钮")
    config_find_claim = config_find_reward["claim"]
    Path_list = config_find_claim["PATH"]
    for path in Path_list:
        if find_and_click(
            target_path=path,
            threshold=config_find_claim["THRESHOLD"],
            timeout=config_find_claim["TIMEOUT"],
            interval=config_find_claim["INTERVAL"]
        ):
            logger.info(f"成功点击领取按钮: {path}")
            config_obtained = config_find_reward["obtained"]
            if not find_and_click(
                target_path=config_obtained["PATH"],
                threshold=config_obtained["THRESHOLD"],
                timeout=config_obtained["TIMEOUT"],
                interval=config_obtained["INTERVAL"]
            ):
                logger.debug("未找到获得物品按钮")
            return 
        else:
            logger.warning(f"未找到领取按钮: {path}, 尝试下一个路径")

    logger.debug("所有领取按钮路径均未找到")
    return

def get_task_reward() -> bool:
    """从主页进入任务页面, 领取奖励后返回主页。"""
    logger.info("开始从主页进入任务页面")
    config_find_reward = config["tasks"]["goto_reward"]["task"]

    # 进入任务页面
    if not find_and_click(
        target_path=config_find_reward["PATH"],
        threshold=config_find_reward["THRESHOLD"],
        timeout=config_find_reward["TIMEOUT"],
        interval=config_find_reward["INTERVAL"]
    ):
        logger.error("未找到任务按钮，无法进入任务页面")
        print("未找到任务按钮，无法进入任务页面")
        return False

    # 进入每日活跃页面
    config_day = config_find_reward["day"]
    if not find_and_click(
        target_path=config_day["PATH"],
        threshold=config_day["THRESHOLD"],
        timeout=config_day["TIMEOUT"],
        interval=config_day["INTERVAL"]
    ):
        logger.error("无法进入每日活跃页面")
        print("无法进入每日活跃页面")

    # 全部领取奖励 (日活)
    click_claim(config_find_reward)

    # 进入周活页面
    config_week = config_find_reward["week"]
    if not find_and_click(
        target_path=config_week["PATH"],
        threshold=config_week["THRESHOLD"],
        timeout=config_week["TIMEOUT"],
        interval=config_week["INTERVAL"]
    ):
        logger.error("无法进入周活页面")

    # 全部领取奖励 (周活)
    click_claim(config_find_reward)

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