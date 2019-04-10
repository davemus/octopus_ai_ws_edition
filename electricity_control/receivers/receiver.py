import json
import datetime
from abc import ABC, abstractmethod


def date_parser(dct):
    if 'date' in dct:
        dct['date'] = datetime.datetime.fromtimestamp(dct['date'])
    return dct


class Receiver(ABC):

    def __iter__(self):
        for i in self._iter_f():
            yield json.loads(i, object_hook=date_parser)

    @abstractmethod
    def _iter_f(self):
        raise NotImplementedError()

    @abstractmethod
    def start(self):
        raise NotImplementedError()
