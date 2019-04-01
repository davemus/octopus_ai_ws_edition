import json


class Receiver:

    def __iter__(self):
        for i in self._iter_f():
            yield json.loads(i)

    def _iter_f(self):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()
