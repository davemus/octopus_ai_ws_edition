import pickle

from keras.engine.saving import model_from_json

import os
from .model import Model
import numpy as np
from loguru import logger
from typing import Dict, Any
import keras
import json

columns = ['Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity',
           'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']


class LSTMModel(Model):

    def __init__(self, path_to_weights_folder):
        self.path_to_weights_folder = path_to_weights_folder
        self.model = None
        self.scaler = None

    def predict(self, data: Dict[str, Any]):
        data = np.array([data[k] for k in columns])
        data = np.expand_dims(data, 0)
        return

    def load(self):
        model_structure_path = os.path.join(self.path_to_weights_folder, 'model.json')
        model_weights_path = os.path.join(self.path_to_weights_folder, 'weights.hd5')
        scaler_path = os.path.join(self.path_to_weights_folder, 'scaler.pkl')
        with open(model_structure_path, 'r') as f:
            model_json = json.load(f)
        self.model = model_from_json(model_json)
        self.model.load_weights(model_weights_path)
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
