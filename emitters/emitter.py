import json
import time
from multiprocessing import Process
import datetime
import pandas as pd
from typing import Sequence
from abc import ABC, abstractmethod


def encode_datetime(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.timestamp()
    return str(obj)


class Emitter(ABC, Process):
    """

    """

    def __init__(self, period: str, start_date: str, end_date: str, delay: int=5, loop: bool=False,
                 data_path: str='/app/data/household_power_consumption.txt', columns_to_emit: Sequence[str]=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.delay = delay
        self.loop = loop
        self.data_path = data_path
        self.data = None
        if columns_to_emit is None:
            columns_to_emit = ['Global_active_power']
        self.columns_to_emit = columns_to_emit
        self._stop = False

    def load_data(self):
        data = pd.read_csv(self.data_path, sep=';',
                           parse_dates={'dt': ['Date', 'Time']}, infer_datetime_format=True,
                           low_memory=False, na_values=['nan', '?'], index_col='dt')
        data = data[self.start_date:self.end_date]
        self.data = data[self.columns_to_emit].resample(self.period).apply(sum)

    @abstractmethod
    def _pre_start(self):
        raise NotImplementedError()

    def _loop(self):
        for data_point, date in zip(self.data.values, self.data.index.values):
            data_to_send = {column: val for column, val in zip(self.columns_to_emit, data_point)}
            data_to_send['date'] = date.astype(datetime.datetime) / 1000000000  # TODO align data here
            self._send(json.dumps(data_to_send, default=encode_datetime))
            time.sleep(self.delay)
            if self._stop:
                break

    @abstractmethod
    def _send(self, data):
        raise NotImplementedError()

    def stop(self):
        self._stop = True

    def run(self):
        self.load_data()
        self._pre_start()
        self._loop()
        while self.loop and not self._stop:
            self._loop()
