from .model import Model
import pickle
from fbprophet import Prophet


class ProphetModel(Model):

    def __init__(self, model_path, data_freq, prediction_period=500):
        self.model: Prophet = None
        self.model_path = model_path
        self.data_freq = data_freq
        self.prediction_period = prediction_period
        self.forecast = None

    def predict(self, data):
        pass

    def load(self):
        with open(self.model_path, 'rb') as f:
            self.model: Prophet = pickle.load(f)
        prediction_df = self.model.make_future_dataframe(periods=self.prediction_period, freq=self.data_freq)
        self.forecast = self.model.predict(prediction_df)
