from .receiver import Receiver
from redis import StrictRedis


class RedisReceiver(Receiver):

    def __init__(self, redis_url, channel):
        self.redis_url = redis_url
        self.channel = channel
        self.subscriber = None

    def __iter__(self):
        return iter(self.subscriber.listen())

    def start(self):
        redis = StrictRedis.from_url(self.redis_url)
        self.subscriber = redis.pubsub()
        self.subscriber.subscribe(self.channel)
