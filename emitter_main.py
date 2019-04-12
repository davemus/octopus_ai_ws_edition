from datetime import datetime
import numpy as np
from emitters import MqttEmitter, RedisEmitter
from loguru import logger

redis_url = 'redis://redis:6379'
mqtt_host = 'mosquitto'
mqtt_port = 1883
hourly_mean = 'data_h_m'
daily_sum = 'data_d_s'
daily_mean = 'data_d_m'

start_date = '2010-10-26'
end_date = '2010-11-26'

redis_emitter = RedisEmitter('redis://redis:6379', hourly_mean, 'h', start_date, end_date,
                             columns_to_emit=['Global_active_power', 'Global_reactive_power', 'Voltage',
                                              'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'],
                             aggregation_fn=np.mean)
redis_emitter.start()

logger.info('SAS')

redis_emitter = RedisEmitter('redis://redis:6379', daily_sum, 'd', start_date, end_date,
                             columns_to_emit=['Global_active_power', 'Global_reactive_power', 'Voltage',
                                              'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'],
                             aggregation_fn=np.sum)
redis_emitter.start()

mqtt_emitter = MqttEmitter(mqtt_host, mqtt_port, daily_mean, 'd', start_date, end_date,
                           columns_to_emit=['Global_active_power', 'Global_reactive_power', 'Voltage',
                                            'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'],
                           aggregation_fn=np.mean)
mqtt_emitter.start()
