from datetime import datetime
from emitters import *

redis_emitter = MqttEmitter('mosquitto', 1883, 'test', 'd', '2006-12-26', '2007-12-26')
redis_emitter.start()
