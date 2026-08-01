import cv2
import numpy as np


def show_image(
    image: np.ndarray,
    window_name: str = "Image",
    wait: int = 0,
) -> None:
    """
    显示一张 OpenCV 图片。

    Parameters
    ----------
    image
        OpenCV BGR 图像。
    window_name
        显示窗口名称。
    wait
        cv2.waitKey() 的等待时间。
        0 表示一直等待按键。
    """
    cv2.imshow(window_name, image)
    cv2.waitKey(wait)
    cv2.destroyWindow(window_name)

