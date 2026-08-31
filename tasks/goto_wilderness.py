"""
进入不休荒原依次领取奖励
不休荒原目标用: targets/button/wilderness.png

目标识别在targets/button/wilderness
依次点击1.png, 2.png, 3.png

然后按"返回"按钮返回主页
"""

from core.actions import find_and_click
from core.button_click import (
    click_home,
    click_wilderness,
)
from core.config import config
from core.logger import logger
from time import sleep

def _click_k() -> bool:
    """依次点击不休荒原的三个奖励按钮"""
    logger.info("开始依次点击不休荒原的三个奖励按钮")
    wilderness_config = config["tasks"]["goto_wilderness"]
    for i in range(1, 4):
        sleep(1)  # 等待界面加载
        button_key = i
        button_config = wilderness_config[button_key]
        if not find_and_click(
            target_path=button_config["PATH"],
            threshold=button_config["THRESHOLD"],
            timeout=button_config["TIMEOUT"],
            interval=button_config["INTERVAL"],
            click_once=True,
        ):
            logger.error(f"未找到不休荒原 {button_key} 按钮")
            return False
    return True

def goto_wilderness() -> bool:
    """从主页进入不休荒原，依次领取奖励后返回主页。"""
    logger.info("开始从主页进入不休荒原")

    if not click_wilderness():
        logger.error("未找到不休荒原按钮")
        return False
    
    if not _click_k():
        logger.error("在不休荒原中未找到奖励按钮")
        return False

    if not click_home():
        logger.error("未找到返回按钮，无法从不休荒原返回主页")
        return False

    logger.info("不休荒原奖励领取完成，已返回主页")
    return True


if __name__ == "__main__":
    from core.window import find_open_window

    print("开始测试 goto_wilderness 函数")
    find_open_window(title_keywords=["MuMu模拟器"])
    if goto_wilderness():
        print("不休荒原测试完成")
    else:
        print("不休荒原测试失败")
