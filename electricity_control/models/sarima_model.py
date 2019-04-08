from .model import Model
import pickle
import pandas as pd


class SarimaModel(Model):

    def __init__(self, path_to_model, start_date, pred_freq, pred_periods, prediction_postprocess):
        self.model = None
        self.start_date = start_date
        self.pred_freq = pred_freq
        self.path_to_model = path_to_model
        self.pred_periods = pred_periods
        self.forecast = None
        self.prediction_postprocess = prediction_postprocess

    def predict(self, data):
        pass

    def load(self):
        with open(self.path_to_model, 'rb') as f:
            self.model = pickle.load(f)
        forecast_dates = pd.date_range(self.start_date, periods=self.pred_periods, freq=self.pred_freq)
        forecast_data = self.model.forecast(self.pred_periods)
        self.forecast = pd.DataFrame.from_dict({'date': forecast_dates, 'forecast': forecast_data}, orient='columns')
