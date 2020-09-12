from typing import Optional, Union

from easydata.config.loader import ConfigLoader
from easydata.utils import config


class ConfigMixin:
    _config: Optional[ConfigLoader] = None

    def has_config_initialized(self):
        return bool(self._config)

    @property
    def config(self):
        if not self._config:
            self._config = config

        return self._config

    def init_config(self, config_obj: Union[dict, ConfigLoader]):
        if isinstance(config_obj, ConfigLoader):
            self._config = config_obj
        else:
            new_config = config.copy()

            new_config.from_dict(config_obj)

            self._config = new_config
