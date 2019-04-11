from electricity_control.models import LGBMModel, IdentityModel, LSTMModel, SarimaModel, ProphetModel
from electricity_control.receivers import RedisReceiver, MqttReceiver
from electricity_control.recorders import RedisRecorder, PrometheusRecorder
from electricity_control.worker import Worker
from electricity_control.bokeh_visualiser import BokehVisualiser

redis_url = 'redis://redis:6379'
hourly_mean = 'data_h_m'
hourly_sum = 'data_h_s'
daily_sum = 'data_d_s'

workers = [Worker(LSTMModel('models/lstm_keras'), RedisReceiver(redis_url, 'data_h'),
                  [PrometheusRecorder('lstm_keras_h', 8000),
                   RedisRecorder('redis://redis:6379', 'lstm_keras_h')]),

           Worker(LGBMModel('models/light_gbm/weights.gbm', {}), RedisReceiver(redis_url, 'daily_sum'),
                  [PrometheusRecorder('lgmb_d', 8001),
                   RedisRecorder(redis_url, 'lgmb_d')]),

           Worker(ProphetModel('models/fbprophet/model_wb.pkl', 'd', 0.6665092992069518),
                  RedisReceiver(redis_url, 'daily_sum'),
                  [PrometheusRecorder('fbprophet_d', 8002),
                   RedisRecorder(redis_url, 'fbprophet_d')]),

           Worker(SarimaModel('models/sarima/model.sa', 'd', 30), RedisReceiver(redis_url, 'daily_sum'),
                  [PrometheusRecorder('sarima_d', 8004),
                   RedisRecorder(redis_url, 'sarima_d')]),

           Worker(IdentityModel(), RedisReceiver(redis_url, hourly_mean),
                  [PrometheusRecorder(hourly_mean, 8002)]),
           Worker(IdentityModel(), RedisReceiver(redis_url, hourly_sum),
                  [PrometheusRecorder(hourly_sum, 8003)]),
           Worker(IdentityModel(), RedisReceiver(redis_url, daily_sum),
                 [PrometheusRecorder(daily_sum, 8003)])
           ]

for worker in workers:
    worker.start()

worker = Worker(LSTMModel('models/lstm_keras_d'), RedisReceiver(redis_url, 'data_d'),
                [PrometheusRecorder('lstm_keras_d', 8001),
                 RedisRecorder(redis_url, 'lstm_keras_d')])
worker.start()

worker = Worker(LSTMModel('models/lgbm_d'), RedisReceiver(redis_url, 'data_d'),
                [PrometheusRecorder('lgbm_d', 8000),
                 RedisRecorder(redis_url, 'lgbm_d')])
worker.start()
