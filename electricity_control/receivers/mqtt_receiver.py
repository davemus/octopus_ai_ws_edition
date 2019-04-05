from queue import Queue

import paho.mqtt.client as mqtt
from .receiver import Receiver


class MqttReceiver(Receiver):

    def __init__(self, url, port, channel, keep_alive=60):
        self.url = url
        self.port = port
        self.keep_alive = keep_alive
        self.channel = channel
        self.client: mqtt.Client = None
        self.queue = Queue()

    def _iter_f(self):
        while True:
            msg = self.queue.get()
            yield msg

    def on_message(self, client, userdata, msg):
        self.queue.put(msg.payload)

    def start(self):
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(self.url, self.port, self.keep_alive)
        self.client.subscribe(self.channel)
        self.client.loop_start()
