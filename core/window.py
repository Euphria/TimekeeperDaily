"""窗口管理：查找、等待并激活游戏窗口。"""

from dataclasses import dataclass
import time
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except (AttributeError, OSError):
    ctypes.windll.user32.SetProcessDPIAware()

import win32con
import win32gui

from core.logger import logger
from core.debug  import show_image


MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 350


@dataclass(frozen=True)
class WindowInfo:
    hwnd: int
    title: str
    left: int
    top: int
    width: int
    height: int


def list_visible_windows() -> list[tuple[int, str]]:
    """列出当前可见且有标题的窗口。"""
    windows: list[tuple[int, str]] = []

    def callback(hwnd: int, _: object) -> None:
        if not win32gui.IsWindowVisible(hwnd):
            return

        title = win32gui.GetWindowText(hwnd).strip()

        if title:
            windows.append((hwnd, title))

    win32gui.EnumWindows(callback, None)
    return windows


def get_window_info(hwnd: int, title: str) -> WindowInfo | None:
    """读取窗口位置和尺寸，尺寸无效时返回 None。"""
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)

    width = right - left
    height = bottom - top

    if width <= 0 or height <= 0:
        return None

    return WindowInfo(
        hwnd=hwnd,
        title=title,
        left=left,
        top=top,
        width=width,
        height=height,
    )


def is_usable_window(
    window: WindowInfo,
    min_width: int = MIN_WINDOW_WIDTH,
    min_height: int = MIN_WINDOW_HEIGHT,
) -> bool:
    """判断窗口尺寸是否足够用于截图识别。"""
    return window.width >= min_width and window.height >= min_height


def find_open_window(
    title_keywords: list[str] = ["MuMu模拟器"],
    min_width: int = MIN_WINDOW_WIDTH,
    min_height: int = MIN_WINDOW_HEIGHT,
) -> WindowInfo | None:
    """
    根据窗口标题关键字查找游戏窗口。
    """
    keywords = tuple(keyword.lower() for keyword in title_keywords)

    for hwnd, title in list_visible_windows():
        title_lower = title.lower()

        if not any(keyword in title_lower for keyword in keywords):
            continue

        activate_window(get_window_info(hwnd, title))

        window = get_window_info(hwnd, title)

        return window

    return None


def wait_for_game_window(
    timeout: float = 60.0,
    interval: float = 1.0,
    min_width: int = MIN_WINDOW_WIDTH,
    min_height: int = MIN_WINDOW_HEIGHT,
) -> WindowInfo | None:
    """
    等待游戏窗口出现，并确认窗口尺寸足够截图识别。
    """
    logger.info("等待游戏窗口出现")

    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        window = find_open_window(
            min_width=min_width,
            min_height=min_height,
        )

        if window is not None:
            logger.info(
                "找到游戏窗口: title=%s, position=(%d, %d), size=%dx%d",
                window.title,
                window.left,
                window.top,
                window.width,
                window.height,
            )
            return window

        time.sleep(interval)

    logger.error("等待游戏窗口超时: timeout=%.1f 秒", timeout)
    return None


def activate_window(window: WindowInfo) -> bool:
    """
    将游戏窗口恢复并置于前台。
    """
    try:
        if win32gui.IsIconic(window.hwnd):
            win32gui.ShowWindow(window.hwnd, win32con.SW_RESTORE)
            time.sleep(0.5)

        win32gui.ShowWindow(window.hwnd, win32con.SW_SHOW)

        try:
            win32gui.SetForegroundWindow(window.hwnd)
            logger.info("已激活游戏窗口")
        except Exception:
            logger.warning("设置游戏窗口为前台失败，将继续尝试截图识别", exc_info=True)

        return True
    except Exception:
        logger.exception("激活游戏窗口失败")
        return False


def is_in_homepage() -> bool:
    """单次判断当前游戏窗口是否处于主页。"""
    from core.capture import capture_window
    from core.config import config
    from core.matcher import find_target

    window_config = config["core"]["window"]
    window = find_open_window(
        title_keywords=window_config["title_keywords"],
    )

    if window is None:
        logger.info("未找到游戏窗口，当前不在主页")
        return False

    homepage_config = window_config["homepage"]
    result = find_target(
        image=capture_window(window),
        target_relative_path=homepage_config["PATH"],
        threshold=homepage_config["THRESHOLD"],
    )

    logger.info(
        "主页判断完成: is_in_homepage=%s, confidence=%.4f",
        result.found,
        result.confidence,
    )
    return result.found



if __name__ == "__main__":
    from pathlib import Path

    import cv2

    from core.capture import capture_window

    lists = list_visible_windows()
    window = find_open_window(title_keywords=["MuMu模拟器"])
    print(f"找到窗口: {window}")

    print("Is Homepage?", is_in_homepage())

    # def show_window(window: WindowInfo) -> None:
    #     """
    #     调试函数：直接截取并显示指定窗口。

    #     仅用于 window.py 测试，不依赖其他模块。
    #     """
    #     image = capture_window(window)

    #     show_image(image, window.title)

    # if window is not None:
    #     show_window(window)
