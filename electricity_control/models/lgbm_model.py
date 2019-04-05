from .model import Model
from lightgbm import Booster


class LGBMModel(Model):

    def __init__(self, path_to_weights):
        self.path_to_weights = path_to_weights
        self.

    def prepare_data(self):
        pass

    def predict(self, data):
        pass

    def load(self):
        pass
