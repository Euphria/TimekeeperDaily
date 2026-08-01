"""游戏启动：在桌面快捷方式中查找游戏并发送启动命令。"""

import os
from pathlib import Path

from core.logger import logger
from core.window import list_visible_windows


def _get_desktop_paths() -> list[Path]:
    """
    获取当前 Windows 用户可能使用的桌面目录。

    支持普通桌面、OneDrive 英文桌面和 OneDrive 中文桌面。
    """
    home = Path.home()

    candidates = [
        home / "Desktop",
        home / "桌面",
        home / "OneDrive" / "Desktop",
        home / "OneDrive" / "桌面",
    ]

    desktop_paths = [
        path
        for path in candidates
        if path.exists() and path.is_dir()
    ]

    logger.debug(
        "检测到的桌面目录: %s",
        [str(path) for path in desktop_paths],
    )

    return desktop_paths


def find_game_shortcut(keyword: str) -> Path | None:
    """
    在桌面目录中查找名称包含指定关键字的 Windows 快捷方式。

    Parameters
    ----------
    keyword:
        快捷方式名称中需要包含的关键字。

    Returns
    -------
    Path | None
        找到时返回快捷方式路径，否则返回 None。
    """
    desktop_paths = _get_desktop_paths()

    if not desktop_paths:
        logger.error("未找到有效的桌面目录")
        return None

    keyword_lower = keyword.lower()

    for desktop_path in desktop_paths:
        logger.debug("正在搜索桌面目录: %s", desktop_path)

        try:
            for file_path in desktop_path.iterdir():
                if not file_path.is_file():
                    continue

                if file_path.suffix.lower() != ".lnk":
                    continue

                if not any(k in file_path.stem.lower() for k in keyword_lower):
                    continue

                logger.info("找到游戏快捷方式: %s", file_path)
                return file_path

        except OSError:
            logger.exception("读取桌面目录失败: %s", desktop_path)

    logger.error("未找到名称中包含 '%s' 的游戏快捷方式", keyword)
    return None


def launch_game(keyword: str = "1999") -> bool:
    """
    查找并启动《重返未来: 1999》的桌面快捷方式。

    Parameters
    ----------
    keyword:
        用于查找快捷方式的关键字，默认为 1999。

    Returns
    -------
    bool
        启动命令发送成功时返回 True, 否则返回 False。
    """
    logger.info("开始启动《重返未来: 1999》")

    shortcut = find_game_shortcut(keyword)

    if shortcut is None:
        logger.error("游戏启动失败: 未找到游戏快捷方式")
        return False

    try:
        os.startfile(shortcut)
    except OSError:
        logger.exception("游戏启动失败，快捷方式路径: %s", shortcut)
        return False

    logger.info("已发送游戏启动指令")
    return True

def close_game(keyword: str) -> bool:
    """
    关闭游戏窗口。

    Returns
    -------
    bool
        成功关闭游戏窗口时返回 True, 否则返回 False。
    """
    logger.info("开始关闭游戏")
    windows = list_visible_windows()

    for hwnd, title in windows:
        if keyword in title:
            window = type('Window', (), {'hwnd': hwnd, 'title': title})()
            break

    if window is None:
        logger.warning("未找到游戏窗口，可能已关闭")
        return True

    try:
        import win32gui

        win32gui.PostMessage(window.hwnd, 0x0010, 0, 0)  # WM_CLOSE
        logger.info("已发送关闭游戏窗口指令: title=%s", window.title)
        return True
    except Exception:
        logger.exception("关闭游戏窗口失败: title=%s", window.title)
        return False

if __name__ == "__main__":
    # 测试游戏启动功能
    from time import sleep

    if launch_game(keyword="1999"):
        print("游戏启动指令发送成功")
    else:
        print("游戏启动指令发送失败")

    sleep(6)  # 等待 6 秒后尝试关闭游戏

    if close_game(keyword="MuMu模拟器"):
        print("游戏关闭指令发送成功")
    else:
        print("游戏关闭指令发送失败")