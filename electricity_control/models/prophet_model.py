from .model import Model
import pickle
from fbprophet import Prophet
from loguru import logger
import numpy as np


class ProphetModel(Model):

    def __init__(self, model_path, data_freq, prediction_period=500):
        self.model: Prophet = None
        self.model_path = model_path
        self.data_freq = data_freq
        self.prediction_period = prediction_period
        self.forecast = None

    def predict(self, data):
        try:
            logger.debug(f'Data date {data["date"]}')
            ind = self.forecast[self.forecast['ds'] == data['date']].index
            if len(ind) == 0:
                ind = 0
            logger.debug(f'Ind: {ind}')
            logger.debug(f'Ind: {ind+1}')
            ret_val = self.forecast.iloc[ind+1, 1]

        except KeyError:
            ret_val = 0
        return ret_val

    def load(self):
        with open(self.model_path, 'rb') as f:
            self.model: Prophet = pickle.load(f)
        prediction_df = self.model.make_future_dataframe(periods=self.prediction_period, freq=self.data_freq)
        self.forecast = self.model.predict(prediction_df[-self.prediction_period:])[['ds', 'yhat']]
        logger.debug(self.forecast.shape)
        logger.debug(self.forecast.head())
        logger.debug(self.forecast.tail())
