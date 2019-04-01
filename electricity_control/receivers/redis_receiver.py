from .receiver import Receiver
from redis import StrictRedis
import json


class RedisReceiver(Receiver):

    def __init__(self, redis_url, channel):
        self.redis_url = redis_url
        self.channel = channel
        self.subscriber = None

    def _iter_f(self):
        for msg in self.subscriber.listen():
            if msg['type'] == 'message':
                yield json.loads(msg['data'])

    def start(self):
        redis = StrictRedis.from_url(self.redis_url)
        self.subscriber = redis.pubsub()
        self.subscriber.subscribe(self.channel)

# Got {'type': 'message', 'pattern': None, 'channel': b'test', 'data': b'{"Global_active_power": 1269.2360000000006}'}
