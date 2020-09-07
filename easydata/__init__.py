import importlib
import os

from easydata.default import Config
from easydata.default import config as default_config

__version__ = "0.0.3"

config = Config()

config.from_module(default_config)

custom_config_module_path = os.environ.get("ED_CONFIG_PATH")

if custom_config_module_path:
    custom_config_module = importlib.import_module(custom_config_module_path)

    config.from_module(custom_config_module)
