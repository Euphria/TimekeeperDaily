""""
基于先验知识设置一条从homepage到战斗界面的路径, 并返回homepage
路径中包含一系列按钮的点击顺序。
"""
from core.button_click import (
    click_return,
    click_home,
    click_enter,
    click_resource,
    click_MA,
    click_TP,
    click_PA,
    click_start,
    click_replay,
    click_victory,
)
from core.logger import logger
from core.config import config
from core.actions import find_and_click
from time import sleep

# 铸币美学
def goto_MA_start() -> bool:
    """从主页进入“铸币美学”，完成一次关卡并返回主页。"""
    logger.info("开始从主页进入铸币美学页面")

    if not click_enter():
        logger.error("未找到入场按钮，无法进入铸币美学页面")
        return False

    if not click_resource():
        logger.error("未找到资源按钮，无法进入铸币美学页面")
        return False

    if not click_MA():
        logger.error("未找到铸币美学按钮")
        return False

    config_find_06 = config["tasks"]["goto_fight"]["enter"]["resource"]["MA"]["06"]
    if not find_and_click(
        target_path=config_find_06["PATH"],
        threshold=config_find_06["THRESHOLD"],
        timeout=config_find_06["TIMEOUT"],
        interval=config_find_06["INTERVAL"]
    ):
        # logger.error("未找到铸币美学 06 按钮")
        # return False

        if not click_start():
            logger.error("未找到开始按钮")
            return False

    if not click_replay():
        logger.error("未找到复现按钮")
        return False

    sleep(20)

    if not click_victory():
        logger.error("未找到胜利按钮，无法退出战斗")
        return False

    if not click_home():
        logger.error("未找到主页按钮，无法返回主页")
        return False

    logger.info("铸币美学路径执行完成")
    return True

# 尘埃运动
def goto_TP_start() -> bool:
    """
    从主页点击进入尘埃运动页面。

    :return: 是否成功进入尘埃运动页面
    """
    logger.info("开始从主页进入尘埃运动页面")

    # 1, 点击入场按钮
    if not click_enter():
        logger.error("未找到入场按钮，无法进入尘埃运动页面")
        return False

    # 2, 点击资源按钮
    if not click_resource():
        logger.error("未找到资源按钮，无法进入尘埃运动页面")
        return False

    # 3, 点击尘埃运动按钮
    if not click_TP():
        logger.error("未找到尘埃运动按钮，无法进入尘埃运动页面")
        return False

    logger.info("成功进入尘埃运动页面")

    # 4, 点击06按钮
    config_find_06 = config["tasks"]["goto_fight"]["enter"]["resource"]["TP"]["06"]
    if not find_and_click(
        target_path=config_find_06["PATH"],
        threshold=config_find_06["THRESHOLD"],
        timeout=config_find_06["TIMEOUT"],
        interval=config_find_06["INTERVAL"]
    ):
        # logger.error("未找到06按钮, 无法进入start页面")
        # return False

        # 5, 点击开始按钮
        if not click_start():
            logger.error("未找到开始按钮, 无法进入复现页面")
            return False

    # 6, 点击复现按钮
    if not click_replay():
        logger.error("未找到复现按钮, 无法进入战斗页面")
        return False

    sleep(20)  # 等待战斗结束

    if not click_victory():
        logger.error("未找到胜利按钮, 无法退出战斗")
        return False

    if not click_home():
        logger.error("未找到主页按钮, 无法返回主页")
        return False
    
    return True

# 意志解析
def goto_PA_start() -> bool:
    """
    从主页进入意志解析页面，完成一次关卡并返回主页。
    """
    logger.info("开始从主页进入意志解析页面")

    if not click_enter():
        logger.error("未找到入场按钮，无法进入意志解析页面")
        return False

    if not click_resource():
        logger.error("未找到资源按钮，无法进入意志解析页面")
        return False

    if not click_PA():
        logger.error("未找到意志解析按钮")
        return False

    config_find_07 = config["tasks"]["goto_fight"]["enter"]["resource"]["PA"]["07"]
    if not find_and_click(
        target_path=config_find_07["PATH"],
        threshold=config_find_07["THRESHOLD"],
        timeout=config_find_07["TIMEOUT"],
        interval=config_find_07["INTERVAL"]
    ):
        # logger.error("未找到意志解析 07 按钮")
        # return False

        if not click_start():
            logger.error("未找到开始按钮")
            return False

    if not click_replay():
        logger.error("未找到复现按钮")
        return False

    sleep(20)

    if not click_victory():
        logger.error("未找到胜利按钮，无法退出战斗")
        return False

    if not click_home():
        logger.error("未找到主页按钮，无法返回主页")
        return False

    logger.info("意志解析路径执行完成")
    return True

if __name__ == "__main__":
    # 仅用于测试 goto_MA_start 函数
    from core.window import find_open_window
    find_open_window(title_keywords=["MuMu模拟器"])
    if goto_PA_start():
        print("完成任务")
    else:
        print("未能完成任务")
