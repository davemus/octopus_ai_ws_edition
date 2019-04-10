from .model import Model
import pickle
from fbprophet import Prophet
from loguru import logger
import numpy as np


def inverse_boxcox(y, lambda_):
    return np.exp(y) if lambda_ == 0 else np.exp(np.log(lambda_ * y + 1) / lambda_)


class ProphetModel(Model):

    def __init__(self, model_path, data_freq, lambda_, prediction_period=500):
        self.model: Prophet = None
        self.model_path = model_path
        self.data_freq = data_freq
        self.prediction_period = prediction_period
        self.forecast = None
        self.lambda_ = lambda_

    def predict(self, data):
        try:
            ind = self.forecast[self.forecast['ds'] == data['date']].index
            ret_val = inverse_boxcox(self.forecast.iloc[ind+1, 1], self.lambda_).values[0]
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
