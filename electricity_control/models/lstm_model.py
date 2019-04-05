from .model import Model
from loguru import logger


class LSTMModel(Model):

    def predict(self, data):
        logger.info(f'Got {data}')
        return data['Global_active_power'] + 0.5

    def load(self):
        pass
