from electricity_control.models import LGBMModel, IdentityModel, LSTMModel, SarimaModel, ProphetModel
from electricity_control.receivers import RedisReceiver, MqttReceiver
from electricity_control.recorders import RedisRecorder, PrometheusRecorder
from electricity_control.worker import Worker
from electricity_control.bokeh_visualiser import BokehVisualiser


worker1 = Worker(LSTMModel('models/lstm_keras'), RedisReceiver('redis://redis:6379', 'data_h'),
                [PrometheusRecorder('lstm_keras_h', 8000),
                RedisRecorder('redis://redis:6379', 'lstm_keras_h')])
worker1.start()

worker1 = Worker(LGBMModel('models/light_gbm/weights.gbm', {}), RedisReceiver('redis://redis:6379', 'data_d'),
                [PrometheusRecorder('lgmb_d', 8001),
                RedisRecorder('redis://redis:6379', 'lgmb_d')])
worker1.start()

worker2 = Worker(IdentityModel(), RedisReceiver('redis://redis:6379', 'data_h'),
                [PrometheusRecorder('data_h', 8002)])
worker2.start()

worker2 = Worker(IdentityModel(), RedisReceiver('redis://redis:6379', 'data_d'),
                [PrometheusRecorder('data_d', 8003)])
worker2.start()


# worker = Worker(LSTMModel('models/lstm_keras_d'), RedisReceiver('redis://redis:6379', 'data_d'),
#                 [PrometheusRecorder('lstm_keras_d', 8001),
#                 RedisRecorder('redis://redis:6379', 'lstm_keras_d')])
# worker.start()
#
# worker = Worker(LSTMModel('models/lgbm_d'), RedisReceiver('redis://redis:6379', 'data_d'),
#                 [PrometheusRecorder('lgbm_d', 8000),
#                 RedisRecorder('redis://redis:6379', 'lgbm_d')])
# worker.start()


