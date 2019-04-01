from .model import Model
from loguru import logger


class LSTMModel(Model):

    def predict(self, data):
        logger.info(f'Got {data}')
        return data

    def load(self):
        pass
