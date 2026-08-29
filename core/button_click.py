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
    config_find_enter = config["tasks"]["goto_fight"]["enter"]
    return find_and_click(
        target_path=config_find_enter["PATH"],
        threshold=config_find_enter["THRESHOLD"],
        timeout=config_find_enter["TIMEOUT"],
        interval=config_find_enter["INTERVAL"]
    )


def click_resource() -> bool:
    """查找并点击“资源”按钮。"""
    logger.info("查找并点击“资源”按钮")
    config_find_resource = config["tasks"]["goto_fight"]["enter"]["resource"]
    return find_and_click(
        target_path=config_find_resource["PATH"],
        threshold=config_find_resource["THRESHOLD"],
        timeout=config_find_resource["TIMEOUT"],
        interval=config_find_resource["INTERVAL"]
    )


def click_MA() -> bool:
    """查找并点击“铸币美学”按钮。"""
    logger.info("查找并点击“铸币美学”按钮")
    config_find_ma = config["tasks"]["goto_fight"]["enter"]["resource"]["MA"]
    return find_and_click(
        target_path=config_find_ma["PATH"],
        threshold=config_find_ma["THRESHOLD"],
        timeout=config_find_ma["TIMEOUT"],
        interval=config_find_ma["INTERVAL"]
    )


def click_TP() -> bool:
    """查找并点击“尘埃运动”按钮。"""
    logger.info("查找并点击“尘埃运动”按钮")
    config_find_tp = config["tasks"]["goto_fight"]["enter"]["resource"]["TP"]
    return find_and_click(
        target_path=config_find_tp["PATH"],
        threshold=config_find_tp["THRESHOLD"],
        timeout=config_find_tp["TIMEOUT"],
        interval=config_find_tp["INTERVAL"]
    )


def click_PA() -> bool:
    """查找并点击“意志解析”按钮。"""
    logger.info("查找并点击“意志解析”按钮")
    config_find_pa = config["tasks"]["goto_fight"]["enter"]["resource"]["PA"]
    return find_and_click(
        target_path=config_find_pa["PATH"],
        threshold=config_find_pa["THRESHOLD"],
        timeout=config_find_pa["TIMEOUT"],
        interval=config_find_pa["INTERVAL"]
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

def click_wilderness() -> bool:
    """查找并点击“不休荒原”按钮。"""
    logger.info("查找并点击\"不休荒原\"按钮")
    config_find_wilderness = config["tasks"]["goto_wilderness"]
    return find_and_click(
        target_path=config_find_wilderness["PATH"],
        threshold=config_find_wilderness["THRESHOLD"],
        timeout=config_find_wilderness["TIMEOUT"],
        interval=config_find_wilderness["INTERVAL"]
    )

def click_hoho() -> bool:
    """查找并点击“吼吼点唱机”按钮。"""
    logger.info("查找并点击吼吼点唱机按钮")
    config_find_hoho = config["tasks"]["goto_hoho"]
    return find_and_click(
        target_path=config_find_hoho["PATH"],
        threshold=config_find_hoho["THRESHOLD"],
        timeout=config_find_hoho["TIMEOUT"],
        interval=config_find_hoho["INTERVAL"]
    )

def click_role() -> bool:
    """查找并点击角色。"""
    logger.info("查找并点击角色")
    config_find_role = config["tasks"]["role"]
    return find_and_click(
        target_path=config_find_role["PATH"],
        threshold=config_find_role["THRESHOLD"],
        timeout=config_find_role["TIMEOUT"],
        interval=config_find_role["INTERVAL"],
        click_once=True
    )

if __name__ == "__main__":
    from core.window import find_open_window
    find_open_window(title_keywords=["MuMu模拟器"])
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
    
    # 3,仅用于测试 click_start 函数
    # if click_start():
    #     print("成功点击开始按钮")
    # else:
    #     print("未找到开始按钮")

    # 4,仅用于测试 click_wilderness 函数
    # if click_wilderness():
    #     print("成功点击不休荒原按钮")
    # else:
    #     print("未找到不休荒原按钮")

    # 5,仅用于测试 click_role 函数
    if click_role():
        print("成功点击角色")
    else:
        print("未找到角色")
