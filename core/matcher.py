"""图像匹配：按模板原始尺寸在截图中滑动匹配，返回最高匹配位置。"""

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray

from core.logger import logger


ImageArray = NDArray[np.uint8]

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "targets"


@dataclass(frozen=True)
class MatchResult:
    found: bool
    confidence: float
    x: int | None = None
    y: int | None = None
    width: int = 0
    height: int = 0

    @property
    def center(self) -> tuple[int, int] | None:
        if self.x is None or self.y is None:
            return None

        return (
            self.x + self.width // 2,
            self.y + self.height // 2,
        )


def load_template(relative_path: str) -> ImageArray:
    """读取 targets 目录中的模板图片。"""
    template_path = ASSETS_DIR / relative_path

    template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)

    if template is None:
        raise FileNotFoundError(f"无法读取模板图片: {template_path}")

    return template


def find_target(
    image: ImageArray,
    target_relative_path: str,
    threshold: float = 0.85,
) -> MatchResult:
    """
    在图像中查找目标。

    OpenCV 会按模板原始尺寸从截图左上角开始滑动匹配，返回最高匹配值的位置。
    返回的 x、y 是相对于传入截图左上角的坐标。
    """
    template = load_template(target_relative_path)

    image_height, image_width = image.shape[:2]
    template_height, template_width = template.shape[:2]

    if template_width > image_width or template_height > image_height:
        logger.warning(
            "模板尺寸大于截图尺寸: target=%s, template=%dx%d, image=%dx%d",
            target_relative_path,
            template_width,
            template_height,
            image_width,
            image_height,
        )
        return MatchResult(False, 0.0)

    result = cv2.matchTemplate(
        image,
        template,
        cv2.TM_CCOEFF_NORMED,
    )

    _, max_confidence, _, max_location = cv2.minMaxLoc(result)
    max_confidence = float(max_confidence)
    found = max_confidence >= threshold

    logger.debug(
        "模板滑动匹配: target=%s, confidence=%.4f, threshold=%.4f, location=(%d, %d), found=%s",
        target_relative_path,
        max_confidence,
        threshold,
        max_location[0],
        max_location[1],
        found,
    )

    if not found:
        return MatchResult(
            found=False,
            confidence=max_confidence,
        )

    return MatchResult(
        found=True,
        confidence=max_confidence,
        x=max_location[0],
        y=max_location[1],
        width=template_width,
        height=template_height,
    )
