"""登录任务：全屏查找开始按钮，点击后等待游戏主页出现。"""

from core.actions import (
    wait_for_target,
    find_and_click,
    wait_for_target_disappear,
)
from core.logger import logger

def login_game(config: dict) -> bool:
    """
    通过全屏模板匹配完成登录。

    流程为：
    1. 等待登录界面出现
    2. 查找开始游戏按钮。
    3. 点击开始游戏按钮。
    4. 确认login界面消失
    """

    # 等待登录界面出现
    logger.info("等待登录界面出现")
    if not wait_for_target(
        target_path=config["LOGIN_TARGET"],
        threshold=config["LOGIN_THRESHOLD"],
        timeout=config["LOGIN_TIMEOUT"],
        interval=config["LOGIN_INTERVAL"],
    ):
        logger.error("登录界面未出现，登录失败")
        return False

    # 查找并点击开始游戏按钮
    logger.info("查找并点击开始游戏按钮")
    if not find_and_click(
        target_path=config["LOGIN_TARGET"],
        threshold=config["LOGIN_THRESHOLD"],
        timeout=config["LOGIN_TIMEOUT"],
        interval=config["LOGIN_INTERVAL"],
    ):
        logger.error("未找到开始游戏按钮，登录失败")
        return False

    # 等待login界面消失
    logger.info("等待login界面消失")
    if not wait_for_target_disappear(
        target_path=config["LOGIN_TARGET"],
        threshold=config["LOGIN_THRESHOLD"],
        timeout=config["LOGIN_TIMEOUT"],
        interval=config["LOGIN_INTERVAL"],
    ):
        logger.error("未等到login界面消失, 登录失败")
        return False

    logger.info("登录成功")
    print("登录成功")
    return True

if __name__ == "__main__":
    # 仅用于测试 login_game 函数
    from core.config import config as app_config
    from core.launch import launch_game
    from core.window import list_visible_windows, activate_window, find_window

    # 如果没有启动游戏，则先启动游戏
    window = find_window(title_keywords=app_config["core"]["window"]["title_keywords"])
    if not window:
        print("未检测到游戏窗口，尝试启动游戏")
        launch_game(keyword=app_config["core"]["launch"]["launch_keyword"])
    else:
        print("已检测到游戏窗口, 窗口置顶, 直接开始login流程")
        activate_window(window)
    login_game(app_config["tasks"]["login"])
