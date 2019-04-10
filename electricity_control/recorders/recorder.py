from abc import ABC, abstractmethod


class Recorder(ABC):

    @abstractmethod
    def record(self, data):
        raise NotImplementedError()

    @abstractmethod
    def start(self):
        raise NotImplementedError()
