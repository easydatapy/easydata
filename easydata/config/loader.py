import importlib
import os
from typing import Optional

from easydata.config import default as default_config


def load_config():
    config_obj = ConfigLoader()

    config_obj.from_module(default_config)

    custom_config_module_path = os.environ.get("ED_CONFIG_PATH")

    if custom_config_module_path:
        custom_config_module = importlib.import_module(custom_config_module_path)

        config_obj.from_module(custom_config_module)

    return config_obj


def _config_dict_from_module(module):
    context = {}
    for module_attr in dir(module):
        if module_attr.isupper() and module_attr.startswith("ED_"):
            context[module_attr] = getattr(module, module_attr)

    return context


class ConfigLoader(dict):
    def __init__(self, config_dict: Optional[dict] = None):
        super().__init__()

        if config_dict:
            self.from_dict(config_dict)

    def from_module(self, config_module):
        config_dict = _config_dict_from_module(config_module)

        self.from_dict(config_dict)

    def from_dict(self, config_dict: dict):
        if config_dict:
            for key, value in config_dict.items():
                if key.isupper() and key.startswith("ED_"):
                    self[key] = value

    def copy(self):
        config_dict_copy = super(ConfigLoader, self).copy()

        return ConfigLoader(config_dict_copy)
