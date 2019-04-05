from .recorder import Recorder
from loguru import logger
from prometheus_client import start_http_server, Gauge


class PrometheusRecorder(Recorder):

    def __init__(self, value_name, port):
        self.summary = Gauge(value_name, f'{value_name} recorder')
        self.port = port

    def record(self, data):
        logger.debug(f'Got {data}')
        self.summary.set(data)

    def start(self):
        start_http_server(self.port)
