from .recorder import Recorder
from redis import StrictRedis
from loguru import logger


class RedisRecorder(Recorder):

    def __init__(self, redis_url, channel):
        self.redis = StrictRedis.from_url(redis_url)
        self.channel = channel

    def record(self, data):
        logger.debug(f'Got {data}')
        self.redis.publish(self.channel, str(data))

    def start(self):
        pass
