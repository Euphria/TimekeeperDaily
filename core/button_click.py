"""
在页面中查找指定按钮并点击
"""

from core.actions import find_and_click
from core.config import config
from core.logger import logger


def click_return(
) -> bool:
    """
    查找并点击返回按钮。

    :param target_path: 返回按钮的图片路径
    :param threshold: 匹配阈值
    :param timeout: 超时时间
    :param interval: 查找间隔
    :return: 是否成功点击返回按钮
    """
    logger.info("查找并点击返回按钮")
    config_find_return = config["tasks"]["return"]
    return find_and_click(
        target_path=config_find_return["PATH"],
        threshold=config_find_return["THRESHOLD"],
        timeout=config_find_return["TIMEOUT"],
        interval=config_find_return["INTERVAL"]
    )

def click_home() -> bool:
    """
    查找并点击主页按钮。

    :return: 是否成功点击主页按钮
    """
    logger.info("查找并点击主页按钮")
    config_find_home = config["tasks"]["home"]
    return find_and_click(
        target_path=config_find_home["PATH"],
        threshold=config_find_home["THRESHOLD"],
        timeout=config_find_home["TIMEOUT"],
        interval=config_find_home["INTERVAL"]
    )

def click_enter() -> bool:
    """
    查找并点击"入场"按钮。

    :return: 是否成功点击"入场"按钮
    """
    logger.info("查找并点击\"入场\"按钮")
    config_find_enter = config["tasks"]["enter"]
    return find_and_click(
        target_path=config_find_enter["PATH"],
        threshold=config_find_enter["THRESHOLD"],
        timeout=config_find_enter["TIMEOUT"],
        interval=config_find_enter["INTERVAL"]
    )


def click_replay() -> bool:
    """查找并点击“再来一次”按钮。"""
    logger.info("查找并点击\"再来一次\"按钮")
    config_find_replay = config["tasks"]["replay"]
    return find_and_click(
        target_path=config_find_replay["PATH"],
        threshold=config_find_replay["THRESHOLD"],
        timeout=config_find_replay["TIMEOUT"],
        interval=config_find_replay["INTERVAL"]
    )

def click_start() -> bool:
    """查找并点击“开始”按钮。"""
    logger.info("查找并点击\"开始\"按钮")
    config_find_start = config["tasks"]["start"]
    return find_and_click(
        target_path=config_find_start["PATH"],
        threshold=config_find_start["THRESHOLD"],
        timeout=config_find_start["TIMEOUT"],
        interval=config_find_start["INTERVAL"]
    )

def click_victory() -> bool:
    """查找并点击“胜利”按钮。"""
    logger.info("查找并点击\"胜利\"按钮")
    config_find_victory = config["tasks"]["victory"]
    return find_and_click(
        target_path=config_find_victory["PATH"],
        threshold=config_find_victory["THRESHOLD"],
        timeout=config_find_victory["TIMEOUT"],
        interval=config_find_victory["INTERVAL"]
    )

if __name__ == "__main__":
    # 1, 仅用于测试 click_return 函数
    # if click_return():
    #     print("成功点击返回按钮")
    # else:
    #     print("未找到返回按钮")

    # 2,仅用于测试 click_home 函数
    # if click_home():
    #     print("成功点击主页按钮")
    # else:
    #     print("未找到主页按钮")

    # 3, 仅用于测试 click_enter 函数
    # if click_enter():
    #     print("成功点击\"入场\"按钮")
    # else:
    #     print("未找到\"入场\"按钮")

    # 4, 仅用于测试 click_resource 函数
    # if click_resource():
    #     print("成功点击\"资源\"按钮")
    # else:
    #     print("未找到\"资源\"按钮")

    # 5, 仅用于测试 click_PA 函数
    # if click_PA():
    #     print("成功点击\"意志解析\"按钮")
    # else:
    #     print("未找到\"意志解析\"按钮")

    # 6, 仅用于测试 click_TP 函数
    if click_TP():
        print("成功点击\"尘埃运动\"按钮")
    else:
        print("未找到\"尘埃运动\"按钮")
