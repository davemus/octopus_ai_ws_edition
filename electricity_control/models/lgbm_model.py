from .model import Model
from lightgbm import Booster
import pandas as pd


def notebook_prepare_data(all_data, new_data):

    return new_data


class LGBMModel(Model):

    def __init__(self, path_to_weights, config, prepare_data_function):
        self.path_to_weights = path_to_weights
        self.config = config
        self.booster: Booster = None
        self.all_data = pd.DataFrame()
        self.prepare_data = prepare_data_function

    def predict(self, data):
        data = self.prepare_data(self.all_data, data)
        if data is not None:
            prediction = self.booster.predict(data)
            return prediction

    def load(self):
        self.booster = Booster(model_file=self.path_to_weights)
