from datetime import datetime
from loguru import logger
from .emitter import Emitter
import paho.mqtt.client as client


class MqttEmitter(Emitter):

    def __init__(self, server_url: str, port: int, channel_name: str, period: str, start_date: str,
                 end_date: str, **kwargs):
        super().__init__(period, start_date, end_date, **kwargs)
        self.server_url = server_url
        self.port = port
        self.channel_name = channel_name
        self.client: 'client.Client' = None

    def _send(self, data):
        logger.info(f'Sending {data} to {self.channel_name}')
        self.client.publish(self.channel_name, data)
        self.client.loop_write()

    def _pre_start(self):
        self.client = client.Client()
        self.client.connect(self.server_url, self.port)
