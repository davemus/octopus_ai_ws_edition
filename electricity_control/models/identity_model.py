from typing import Dict, Any

from loguru import logger
from .model import Model


class IdentityModel(Model):

    def predict(self, data: Dict[str, Any]) -> float:
        return data['Global_active_power']

    def load(self):
        pass
