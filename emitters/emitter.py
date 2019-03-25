import time
from multiprocessing import Process
from datetime import datetime
import pandas as pd
from typing import List


class Emitter(Process):
    """

    """

    def __init__(self, period: str, start_date: datetime, end_date: datetime, delay: int=5, loop: bool=False,
                 data_path: str='/app/data/household_power_consumption.txt', columns_to_emit: List[str]=None,
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
        self.data = data.iloc[self.start_date:self.end_date].resample(self.period)[self.columns_to_emit]

    def _pre_start(self):
        raise NotImplementedError()

    def _loop(self):
        for data_point in self.data.values:
            self._send({column: val for column, val in zip(self.columns_to_emit, data_point)})
            time.sleep(self.delay)

    def _send(self, data):
        raise NotImplementedError()

    def stop(self):
        self._stop = True

    def start(self):
        self.load_data()
        self._pre_start()
        self._loop()
        while self.loop and not self._stop:
            self._loop()
