class Receiver:

    def __iter__(self):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()
