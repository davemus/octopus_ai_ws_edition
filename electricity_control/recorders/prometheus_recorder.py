from .recorder import Recorder
from loguru import logger
from prometheus_client import start_http_server, Gauge


class PrometheusRecorder(Recorder):

    def __init__(self, value_name, port):
        self.value_name = value_name
        self.summary = None
        self.port = port

    def record(self, data):
        logger.debug(f'Got {data}')
        self.summary.set(data)

    def start(self):
        try:
            self.summary = Gauge(self.value_name, f'{self.value_name} recorder')
            start_http_server(self.port)
        except OSError:
            pass
