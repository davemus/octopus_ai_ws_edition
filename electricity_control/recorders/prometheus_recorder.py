from .recorder import Recorder
from loguru import logger


class PrometheusRecorder(Recorder):

    def __init__(self):
        pass

    def record(self, data):
        logger.info(f'Got {data}')

    def start(self):
        pass
