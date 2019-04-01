from datetime import datetime
from emitters import *

redis_emitter = RedisEmitter('redis://redis:6379', 'test', 'd', '2006-12-26', '2007-12-26')
redis_emitter.start()
