from datetime import datetime
import numpy as np
from emitters import *

# redis_emitter = RedisEmitter('redis://redis:6379', 'data_h', 'h', '2006-12-26', '2007-12-26',
#                              columns_to_emit=['Global_active_power', 'Global_reactive_power', 'Voltage',
#                                               'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'],
#                              aggregation_fn=np.mean)
# redis_emitter.start()

redis_emitter = RedisEmitter('redis://redis:6379', 'data_d', 'd', '2010-11-28', '2010-12-27',
                             columns_to_emit=['Global_active_power', 'Global_reactive_power', 'Voltage',
                                              'Global_intensity', 'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3'],
                             aggregation_fn=np.sum)
redis_emitter.start()
