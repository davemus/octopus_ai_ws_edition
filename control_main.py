from electricity_control.models import LGBMModel, IdentityModel, LSTMModel, SarimaModel, ProphetModel
from electricity_control.receivers import RedisReceiver, MqttReceiver
from electricity_control.recorders import RedisRecorder, PrometheusRecorder
from electricity_control.worker import Worker

redis_url = 'redis://redis:6379'
mqtt_host = 'mosquitto'
mqtt_port = 1883
hourly_mean = 'data_h_m'
daily_sum = 'data_d_s'
daily_mean = 'data_d_m'

workers = [
           Worker(LSTMModel('models/lstm_keras_h'), RedisReceiver(redis_url, hourly_mean),
                  [PrometheusRecorder('lstm_keras_h_m', 8001),
                   RedisRecorder('redis://redis:6379', 'lstm_keras_h_m')]),
           Worker(LSTMModel('models/lstm_keras_d_sum'), RedisReceiver(redis_url, daily_sum),
                  [PrometheusRecorder('lstm_keras_d_s', 8002),
                   RedisRecorder('redis://redis:6379', 'lstm_keras_d_s')]),
           Worker(LSTMModel('models/lstm_keras_d_mean'), MqttReceiver(mqtt_host, mqtt_port, daily_mean),
                  [PrometheusRecorder('lstm_keras_d_m', 8003),
                   RedisRecorder('redis://redis:6379', 'lstm_keras_d_m')]),

           Worker(LGBMModel('models/light_gbm_d_sum/weights.gbm', 'models/light_gbm_d_sum/data.pkl'),
                  RedisReceiver(redis_url, daily_sum),
                  [PrometheusRecorder('lgmb_d_s', 8004),
                   RedisRecorder(redis_url, 'lgmb_d_s')]),
           Worker(LGBMModel('models/light_gbm_d_mean/weights.gbm', 'models/light_gbm_d_mean/data.pkl'),
                  MqttReceiver(mqtt_host, mqtt_port, daily_mean),
                  [PrometheusRecorder('lgmb_d_m', 8005),
                   RedisRecorder(redis_url, 'lgmb_d_m')]),
           Worker(LGBMModel('models/light_gbm_h_mean/weights.gbm', 'models/light_gbm_h_mean/data.pkl'),
                  RedisReceiver(redis_url, hourly_mean),
                  [PrometheusRecorder('lgmb_h_m', 8006),
                   RedisRecorder(redis_url, 'lgmb_h_m')]),

           Worker(ProphetModel('models/fbprophet/model.pkl', 'd'),
                  RedisReceiver(redis_url, daily_sum),
                  [PrometheusRecorder('fbprophet_d_s', 8007),
                   RedisRecorder(redis_url, 'fbprophet_d_s')]),

           Worker(SarimaModel('models/sarima/model.sa', 'models/sarima/exog.npy', 'd', 31),
                  MqttReceiver(mqtt_host, mqtt_port, daily_mean),
                  [PrometheusRecorder('sarima_d_m', 8008),
                   RedisRecorder(redis_url, 'sarima_d_m')]),

           Worker(IdentityModel(), RedisReceiver(redis_url, hourly_mean),
                  [PrometheusRecorder(hourly_mean, 8009)]),
           Worker(IdentityModel(), MqttReceiver(mqtt_host, mqtt_port, daily_mean),
                  [PrometheusRecorder(daily_mean, 8010)]),
           Worker(IdentityModel(), RedisReceiver(redis_url, daily_sum),
                  [PrometheusRecorder(daily_sum, 8011)])
           ]

for worker in workers:
    worker.start()

