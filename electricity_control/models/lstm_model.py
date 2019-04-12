import pickle

from keras.engine.saving import model_from_json

import os
from .model import Model
import numpy as np
from loguru import logger
from typing import Dict, Any
import json

columns = ['Global_active_power', 'Global_reactive_power', 'Voltage', 'Global_intensity',
           'Sub_metering_1', 'Sub_metering_2', 'Sub_metering_3']


class LSTMModel(Model):

    def __init__(self, path_to_weights_folder):
        self.path_to_weights_folder = path_to_weights_folder
        self.model = None
        self.scaler = None
        self.all_data = []

    def prepare_data(self, data):
        data = np.array([data[k] for k in columns])
        self.all_data.append(data)
        if len(self.all_data) == 7:
            data = self.scaler.transform(np.array(self.all_data))
            data = np.expand_dims(data, 0)
            self.all_data.pop(0)
            return data

    def predict(self, data: Dict[str, Any]):
        logger.debug(f'Got {data}')
        data = self.prepare_data(data)
        logger.debug(f'Prepared {data}')
        if data is not None:
            prediction = self.model.predict(data)
            logger.debug(f'Prediction {prediction}')
            logger.debug(f'{prediction.shape}, {data[0][0, 1:].shape}')
            prediction = np.concatenate([prediction, np.expand_dims(data[0][0][1:], 0)], axis=-1)
            return self.scaler.inverse_transform(prediction)[0][0]
        return 0

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
