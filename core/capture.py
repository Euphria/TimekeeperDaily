"""截图能力：截取全屏或指定窗口，并转换为 OpenCV 使用的 BGR 图像。"""

from dataclasses import dataclass

import cv2
import mss
import numpy as np
from numpy.typing import NDArray

from core.logger import logger
from core.window import WindowInfo


ImageArray = NDArray[np.uint8]


@dataclass(frozen=True)
class Screenshot:
    image: ImageArray
    left: int
    top: int
    width: int
    height: int


def capture_screen(monitor_index: int = 0) -> Screenshot:
    """
    截取全屏。

    monitor_index=0 表示截取所有显示器组成的虚拟全屏。
    """
    with mss.mss() as screen_capture:
        monitors = screen_capture.monitors

        if monitor_index >= len(monitors):
            raise ValueError(f"显示器序号不存在: {monitor_index}")

        monitor = monitors[monitor_index]
        screenshot = np.asarray(screen_capture.grab(monitor))

    image = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    logger.debug(
        "完成全屏截图: left=%d, top=%d, size=%dx%d, shape=%s",
        monitor["left"],
        monitor["top"],
        monitor["width"],
        monitor["height"],
        image.shape,
    )

    return Screenshot(
        image=image,
        left=monitor["left"],
        top=monitor["top"],
        width=monitor["width"],
        height=monitor["height"],
    )


def capture_window(window: WindowInfo) -> ImageArray:
    """
    截取整个游戏窗口。

    返回 OpenCV BGR 格式图像。
    """
    monitor = {
        "left": window.left,
        "top": window.top,
        "width": window.width,
        "height": window.height,
    }

    with mss.mss() as screen_capture:
        screenshot = np.asarray(screen_capture.grab(monitor))

    image = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)

    logger.debug("完成窗口截图: shape=%s", image.shape)

    return image
