from typing import Dict, Any

from loguru import logger
from .model import Model


class IdentityModel(Model):

    def predict(self, data: Dict[str, Any]) -> float:

        logger.debug(f"Returning identity: {data['Global_active_power']}")
        return data['Global_active_power']

    def load(self):
        pass
