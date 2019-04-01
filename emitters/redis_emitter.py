from .emitter import Emitter
from datetime import datetime
from redis import StrictRedis
from loguru import logger


class RedisEmitter(Emitter):
    """

    """

    def __init__(self, redis_url: str, channel_name: str, period: str, start_date: datetime,
                 end_date: datetime, **kwargs):
        super().__init__(period, start_date, end_date, **kwargs)
        self.redis_url = redis_url
        self.channel_name = channel_name
        self.publisher = None

    def _pre_start(self):
        self.publisher = StrictRedis.from_url(self.redis_url)

    def _send(self, data):
        logger.info(f'Sending {data} to {self.channel_name}')
        self.publisher.publish(self.channel_name, data)
