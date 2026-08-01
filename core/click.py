"""鼠标操作：执行屏幕坐标点击，或把窗口内相对坐标转换后点击。"""

import time

import pydirectinput

from core.logger import logger
from core.window import WindowInfo


# 防止 PyDirectInput 在每次操作后额外暂停太久。
pydirectinput.PAUSE = 0.1


def click_screen_position(x: int, y: int) -> None:
    """点击屏幕上的绝对坐标。"""
    logger.info("点击屏幕坐标: screen=(%d, %d)", x, y)

    pydirectinput.click(
        x=x,
        y=y,
    )


def click_window_position(
    window: WindowInfo,
    relative_x: int,
    relative_y: int,
) -> None:
    """
    点击游戏窗口内的相对坐标。
    """
    screen_x = window.left + relative_x
    screen_y = window.top + relative_y

    logger.info(
        "点击游戏窗口: relative=(%d, %d), screen=(%d, %d)",
        relative_x,
        relative_y,
        screen_x,
        screen_y,
    )

    click_screen_position(screen_x, screen_y)


def sleep(seconds: float) -> None:
    """暂停指定秒数。"""
    time.sleep(seconds)
