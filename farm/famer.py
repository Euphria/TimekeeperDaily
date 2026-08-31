"""基于项目现有图像识别框架循环刷材料。"""

from pathlib import Path
import sys


# 保证可以直接通过 `python farm/famer.py` 运行。
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.actions import find_and_click, wait_for_target
from core.button_click import click_home, click_return
from core.config import load_config
from core.logger import logger
from core.window import find_open_window


FARM_DIR = Path(__file__).resolve().parent
CONFIG_PATH = FARM_DIR / "famer.yaml"


def load_farmer_config(config_path: str | Path = CONFIG_PATH) -> dict:
    """加载刷材料的独立配置。"""
    return load_config(config_path)["farmer"]


def _target_path(relative_path: str) -> str:
    """将 farm 配置中的相对图片路径转换为绝对路径。"""
    return str((FARM_DIR / relative_path).resolve())


def click_configured_target(target_config: dict) -> bool:
    """使用一组刷材料配置查找并点击目标。"""
    return find_and_click(
        target_path=_target_path(target_config["PATH"]),
        threshold=target_config["THRESHOLD"],
        timeout=target_config["TIMEOUT"],
        interval=target_config["INTERVAL"],
    )


def is_configured_target_visible(target_config: dict) -> bool:
    """按配置等待并判断目标是否出现，不执行点击。"""
    result = wait_for_target(
        target_path=_target_path(target_config["PATH"]),
        threshold=target_config["THRESHOLD"],
        timeout=target_config["TIMEOUT"],
        interval=target_config["INTERVAL"],
    )
    return result.found


def return_to_home() -> bool:
    """刷材料停止后依次点击返回和主页。"""
    if not click_return():
        logger.error("未找到返回按钮，无法退出刷材料关卡")
        return False

    if not click_home():
        logger.error("未找到主页按钮，无法返回主页")
        return False

    logger.info("已从刷材料关卡返回主页")
    return True


def enter_farming_stage(farmer_config: dict) -> bool:
    """从主页开始，按顺序点击 1.png 至 4.png。"""
    logger.info("开始进入刷材料关卡")

    for step_number, step_config in enumerate(farmer_config["steps"], start=1):
        if not click_configured_target(step_config):
            logger.error("未找到刷材料步骤 %d: %s", step_number, step_config["PATH"])
            return False
        logger.info("已完成刷材料步骤 %d", step_number)

    return True


def farm_materials(farmer_config: dict | None = None) -> bool:
    """进入关卡并循环点击复现和胜利，直到出现停止画面。

    每轮点击 replay.png 后检查 stop.png；识别到后依次点击
    返回和主页。未识别到时等待 victory.png 并继续下一轮。
    """
    if farmer_config is None:
        farmer_config = load_farmer_config()

    if not enter_farming_stage(farmer_config):
        return False

    completed_rounds = 0
    replay_config = farmer_config["replay"]
    victory_config = farmer_config["victory"]
    stop_config = farmer_config["stop"]

    while True:
        print(f"已完成 {completed_rounds} 轮刷材料，开始第 {completed_rounds + 1} 轮")
        logger.info("开始刷材料第 %d 轮", completed_rounds + 1)

        if not click_configured_target(replay_config):
            logger.error("未找到复现按钮，刷材料流程异常结束")
            return False

        if is_configured_target_visible(stop_config):
            logger.info("识别到刷材料停止画面；已完成 %d 轮", completed_rounds)
            return return_to_home()

        if not click_configured_target(victory_config):
            # 胜利等待期间也可能延迟出现停止画面，再确认一次。
            if is_configured_target_visible(stop_config):
                logger.info("识别到刷材料停止画面；已完成 %d 轮", completed_rounds)
                return return_to_home()

            logger.error(
                "%.1f 秒内未出现胜利或停止画面，刷材料流程异常结束",
                victory_config["TIMEOUT"],
            )
            return False

        completed_rounds += 1
        logger.info("刷材料第 %d 轮完成", completed_rounds)


def main() -> int:
    """刷材料脚本入口。"""
    farmer_config = load_farmer_config()
    window = find_open_window(
        title_keywords=farmer_config["WINDOW_TITLE_KEYWORDS"],
    )

    if window is None:
        logger.error("未找到游戏窗口，无法开始刷材料")
        print("未找到游戏窗口")
        return 1

    if not farm_materials(farmer_config):
        print("刷材料流程异常结束")
        return 1

    print("已检测到停止条件并返回主页")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
