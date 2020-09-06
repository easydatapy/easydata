from typing import Optional, Union

from easydata import config
from easydata.default import Config


class ConfigMixin:
    _config: Optional[Config] = None

    @property
    def config(self):
        if not self._config:
            self._config = config

        return self._config

    def init_config(self, config_obj: Union[dict, Config]):
        if isinstance(config_obj, Config):
            self._config = config_obj
        else:
            new_config = config.copy()

            new_config.from_dict(config_obj)

            self._config = new_config
