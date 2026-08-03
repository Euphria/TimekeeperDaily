"""
加载脚本的配置文件，提供全局配置参数。
"""

import os
from pathlib import Path
import yaml

def load_config(config_path: str | Path) -> dict:
    """
    从 YAML 文件中加载配置。

    Parameters
    ----------
    config_path : str | Path
        配置文件的路径。

    Returns
    -------
    dict
        配置字典。
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"配置文件未找到: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config

config = load_config("config.yaml")
