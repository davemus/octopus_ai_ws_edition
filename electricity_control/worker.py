from multiprocessing import Process
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Type, Sequence
    from electricity_control.recorders.recorder import Recorder
    from electricity_control.receivers.receiver import Receiver
    from electricity_control.models.model import Model


class Worker(Process):

    def __init__(self, model: Model, receiver: Receiver, recorders: Sequence[Recorder], **kwargs):
        super().__init__(**kwargs)
        self.model = model
        self.receiver = receiver
        self.recorders = recorders
        self._stop = False

    def __run_init(self):
        self.model.load()
        self.receiver.start()
        self.data_iterator = iter(self.receiver)
        for recorder in self.recorders:
            recorder.start()

    def stop(self):
        self._stop = False

    def run(self):
        self.__run_init()
        while not self._stop:
            data = next(self.data_iterator)
            prediction = self.model.predict(data)
            for recorder in self.recorders:
                recorder.record(prediction)
