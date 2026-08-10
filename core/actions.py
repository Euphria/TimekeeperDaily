"""通用操作：全屏查找目标图片，并在需要时点击匹配区域中心。"""

import time

from core.capture import Screenshot, capture_screen
from core.click import click_screen_position
from core.config import config
from core.logger import logger
from core.matcher import MatchResult, find_target


config_actions = config["core"]["actions"]


def _wait_for_target_on_screen(
    target_path: str,
    threshold: float,
    timeout: float,
    interval: float,
) -> tuple[MatchResult, Screenshot | None]:
    """循环截取全屏并查找目标，返回本轮最高匹配结果和对应截图。"""
    logger.info(
        "开始全屏等待目标: target=%s, threshold=%.2f, timeout=%.1fs",
        target_path,
        threshold,
        timeout,
    )

    start_time = time.monotonic()
    best_result = MatchResult(found=False, confidence=0.0)
    best_screenshot: Screenshot | None = None

    while time.monotonic() - start_time < timeout:
        screenshot = capture_screen()

        result = find_target(
            image=screenshot.image,
            target_relative_path=target_path,
            threshold=threshold,
        )

        if result.confidence > best_result.confidence:
            best_result = result
            best_screenshot = screenshot

        if result.found:
            logger.info(
                "全屏找到目标: target=%s, confidence=%.4f",
                target_path,
                result.confidence,
            )
            return result, screenshot

        logger.debug(
            "全屏目标尚未出现: target=%s, confidence=%.4f, best=%.4f",
            target_path,
            result.confidence,
            best_result.confidence,
        )

        time.sleep(interval)

    logger.warning(
        "全屏等待目标超时: target=%s, threshold=%.2f, best_confidence=%.4f",
        target_path,
        threshold,
        best_result.confidence,
    )

    return best_result, best_screenshot


def wait_for_target(
    target_path: str,
    threshold: float = 0.80,
    timeout: float = 60.0,
    interval: float = 1.0,
) -> MatchResult:
    """
    全屏等待目标图片出现。

    Returns
    -------
    MatchResult
        找到时返回 found=True: 超时时返回本轮等待中的最高匹配结果。
    """
    result, _ = _wait_for_target_on_screen(
        target_path=target_path,
        threshold=threshold,
        timeout=timeout,
        interval=interval,
    )
    return result

def wait_for_target_disappear(
    target_path: str,
    threshold: float = 0.80,
    timeout: float = 60.0,
    interval: float = 1.0,
) -> bool:
    """
    全屏等待目标图片消失。

    Returns
    -------
    bool
        目标图片消失时返回 True, 超时返回 False。
    """
    logger.info(
        "开始全屏等待目标消失: target=%s, threshold=%.2f, timeout=%.1fs",
        target_path,
        threshold,
        timeout,
    )

    start_time = time.monotonic()

    while time.monotonic() - start_time < timeout:
        screenshot = capture_screen()

        result = find_target(
            image=screenshot.image,
            target_relative_path=target_path,
            threshold=threshold,
        )

        if not result.found:
            logger.info(
                "全屏目标已消失: target=%s, confidence=%.4f",
                target_path,
                result.confidence,
            )
            return True

        logger.debug(
            "全屏目标尚未消失: target=%s, confidence=%.4f",
            target_path,
            result.confidence,
        )

        time.sleep(interval)

    logger.warning(
        "全屏等待目标消失超时: target=%s, threshold=%.2f",
        target_path,
        threshold,
    )
    return False


def find_and_click(
    target_path: str,
    threshold: float = 0.80,
    timeout: float = 60.0,
    interval: float = 1.0,
) -> bool:
    """
    全屏查找目标图片，并点击匹配区域的中心位置。
    """
    result, screenshot = _wait_for_target_on_screen(
        target_path=target_path,
        threshold=threshold,
        timeout=timeout,
        interval=interval,
    )

    if not result.found:
        return False

    if screenshot is None:
        logger.error("匹配成功但未取得截图信息: target=%s", target_path)
        return False

    center = result.center

    if center is None:
        logger.error("匹配成功但未取得中心坐标: target=%s", target_path)
        return False

    screen_x = screenshot.left + center[0]
    screen_y = screenshot.top + center[1]

    logger.info(
        "点击全屏目标: target=%s, confidence=%.4f, image_center=(%d, %d), screen=(%d, %d)",
        target_path,
        result.confidence,
        center[0],
        center[1],
        screen_x,
        screen_y,
    )

    click_deadline = time.monotonic() + timeout

    while time.monotonic() < click_deadline:
        click_screen_position(screen_x, screen_y)
        remaining = click_deadline - time.monotonic()
        disappear_timeout = min(
            config_actions["CLICK_RETRY_INTERVAL"],
            max(0.0, remaining),
        )

        if wait_for_target_disappear(
            target_path=target_path,
            threshold=threshold,
            timeout=disappear_timeout,
            interval=interval,
        ):
            logger.info("目标已消失，停止重复点击: target=%s", target_path)
            return True

        logger.debug("目标仍然存在，继续点击: target=%s", target_path)

    logger.warning(
        "重复点击后目标仍未消失: target=%s, threshold=%.2f",
        target_path,
        threshold,
    )
    return False
