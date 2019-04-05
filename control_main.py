from electricity_control.models import *
from electricity_control.receivers import *
from electricity_control.recorders import *
from electricity_control.worker import Worker
from electricity_control.bokeh_visualiser import BokehVisualiser


worker = Worker(LSTMModel(), RedisReceiver('redis://redis:6379', 'test'),
                [PrometheusRecorder('test_value', 8000),
                RedisRecorder('redis://redis:6379', 'lstm_d')])
worker.start()
