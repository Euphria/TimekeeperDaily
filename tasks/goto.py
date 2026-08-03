""""
基于先验知识设置一条从homepage到目标页面的路径, 并返回homepage
路径中包含一系列按钮的点击顺序。
"""
from core.button_click import (
    click_return,
    click_home,
    click_enter,
    click_resource,
    click_PA,
    click_TP,
)
from core.logger import logger
from core.config import config

def goto_TP() -> bool:
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
    print("成功进入尘埃运动页面")
    return True

if __name__ == "__main__":
    # 仅用于测试 goto_TP 函数
    if goto_TP():
        print("成功进入尘埃运动页面")
    else:
        print("未能进入尘埃运动页面")