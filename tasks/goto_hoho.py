"""进入吼吼点唱机领取专注嘉奖，然后返回主页。"""

from core.actions import find_and_click
from core.button_click import click_hoho, click_return
from core.config import config
from core.logger import logger

from time import sleep


def click_thinking_if_present() -> bool:
    """如果出现“再想想”按钮则点击。"""
    button = config["tasks"]["goto_hoho"]["thinking"]
    return find_and_click(
        button["PATH"], button["THRESHOLD"], button["TIMEOUT"],
        button["INTERVAL"], click_once=True,
    )


def goto_hoho() -> bool:
    """从主页进入吼吼点唱机，领取专注嘉奖后返回主页。"""
    logger.info("开始从主页进入吼吼点唱机")
    hoho_config = config["tasks"]["goto_hoho"]

    if not click_hoho():
        logger.error("未找到吼吼点唱机按钮")
        return False

    sleep(2)  # 等待吼吼点唱机界面加载
    
    claim_all_config = hoho_config["claim_all"]
    if find_and_click(
        target_path=claim_all_config["PATH"],
        threshold=claim_all_config["THRESHOLD"],
        timeout=claim_all_config["TIMEOUT"],
        interval=claim_all_config["INTERVAL"],
        click_once=True,
    ):
        upgrade_config = hoho_config["upgrade"]
        if not find_and_click(
            target_path=upgrade_config["PATH"],
            threshold=upgrade_config["THRESHOLD"],
            timeout=upgrade_config["TIMEOUT"],
            interval=upgrade_config["INTERVAL"],
            click_once=True,
        ):
            logger.debug("未找到升级按钮")
    else:
        logger.error("未找到一键领取按钮")
        return False

    reward_config = hoho_config["reward"]
    if not find_and_click(
        target_path=reward_config["PATH"],
        threshold=reward_config["THRESHOLD"],
        timeout=reward_config["TIMEOUT"],
        interval=reward_config["INTERVAL"],
        click_once=True,
    ):
        logger.error("未找到专注嘉奖按钮")
        return False
    
    # 领奖
    if not find_and_click(
        target_path=claim_all_config["PATH"],
        threshold=claim_all_config["THRESHOLD"],
        timeout=claim_all_config["TIMEOUT"],
        interval=claim_all_config["INTERVAL"],
        click_once=True,
    ):
        logger.debug("所有领取按钮路径均未找到")
        return False

    if click_thinking_if_present():
        logger.info("点击了“再想想”按钮")
    else:
        count_config = hoho_config["count"]
        if not find_and_click(
            target_path=count_config["PATH"],
            threshold=count_config["THRESHOLD"],
            timeout=count_config["TIMEOUT"],
            interval=count_config["INTERVAL"],
            click_once=True,
        ):
            logger.error("未找到“再想想”或计数按钮")
            return False
        logger.info("点击了计数按钮")

    if not click_return():
        logger.error("未找到返回按钮，无法从吼吼点唱机返回主页")
        return False

    logger.info("专注嘉奖领取完成，已返回主页")
    return True


if __name__ == "__main__":
    from core.window import find_open_window

    print("开始测试 goto_hoho 函数")
    find_open_window(title_keywords=["MuMu模拟器"])
    if goto_hoho():
        print("吼吼点唱机测试完成")
    else:
        print("吼吼点唱机测试失败")
