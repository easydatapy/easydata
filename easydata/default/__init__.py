from typing import Optional


def config_dict_from_module(module):
    context = {}
    for module_attr in dir(module):
        if module_attr.isupper() and module_attr.startswith("ED_"):
            context[module_attr] = getattr(module, module_attr)

    return context


class Config(dict):
    def __init__(self, config_dict: Optional[dict] = None):
        super().__init__()

        if config_dict:
            self.from_dict(config_dict)

    def from_module(self, config_module):
        config_dict = config_dict_from_module(config_module)

        self.from_dict(config_dict)

    def from_dict(self, config_dict: dict):
        if config_dict:
            for key, value in config_dict.items():
                self[key] = value

    def copy(self):
        config_dict_copy = super(Config, self).copy()

        return Config(config_dict_copy)
