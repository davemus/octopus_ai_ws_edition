from electricity_control.models import *
from electricity_control.receivers import *
from electricity_control.recorders import *
from electricity_control.worker import Worker
from electricity_control.bokeh_visualiser import BokehVisualiser


worker = Worker(LSTMModel(), MqttReceiver('mosquitto', 1883, 'test'), [PrometheusRecorder()])
worker.start()
