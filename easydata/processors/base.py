from abc import ABC, abstractmethod
from typing import Any

from easydata.mixins import ConfigMixin


class BaseProcessor(ConfigMixin, ABC):
    model = None

    @abstractmethod
    def parse(self, value: Any) -> Any:
        pass

    def init_model(self, model):
        self.model = model
