from .model import Model
from loguru import logger
import torch
from torch import nn


# TODO fill the code here with the model code
class PyTorchLSTM(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, input):
        pass

    @classmethod
    def load(cls, path_to_weights):
        model = cls()
        state_dict = torch.load(path_to_weights)
        model.load_state_dict(state_dict)
        return model


class LSTMModel(Model):

    def __init__(self, path_to_weights):
        self.path_to_weights = path_to_weights
        self.model = None

    def predict(self, data):
        logger.info(f'Got {data}')
        return data['Global_active_power'] + 0.5

    def load(self):
        self.model = PyTorchLSTM.load(self.path_to_weights)
