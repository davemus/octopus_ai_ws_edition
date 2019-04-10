from .model import Model
import pickle
import numpy as np
import datetime
from loguru import logger

mapping = {'d': 'days', 'H': 'hours'}


class SarimaModel(Model):

    def __init__(self, path_to_model, pred_freq, pred_periods, prediction_postprocess=np.exp):
        self.model = None
        self.pred_freq = pred_freq
        self.timedelta_param_name = mapping[self.pred_freq]
        self.path_to_model = path_to_model
        self.pred_periods = pred_periods
        self.forecast = None
        self.prediction_postprocess = prediction_postprocess

    def predict(self, data):
        try:
            ret_val = self.forecast[data['date'] + datetime.timedelta(**{self.timedelta_param_name: 1})]
        except KeyError as e:
            logger.debug(e)
            ret_val = 0
        return ret_val

    def load(self):
        with open(self.path_to_model, 'rb') as f:
            self.model = pickle.load(f)
        self.forecast = self.prediction_postprocess(self.model.forecast(self.pred_periods))
        logger.debug(self.forecast.head())
        logger.debug(self.forecast.tail())
