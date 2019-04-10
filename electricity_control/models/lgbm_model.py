from .model import Model
from lightgbm import Booster
import pandas as pd
import numpy as np
from loguru import logger


weekday_mean_data = [1453.9886015018553, 1583.1144845385677, 1598.0504237151988, 1430.8047203176632,
                     1530.5532914285714, 1826.5508856767094, 1800.1852442500071]
hour_average_constant = 1603.321093


def mean_encoding(data, cat_feature, real_feature):
    """
    Возвращает словарь, где ключами являются уникальные категории признака cat_feature,
    а значениями - средние по real_feature
    """
    return dict(data.groupby(cat_feature)[real_feature].mean())


def prepare_df(data, target_column='Global_active_power', lag_start=1, lag_end=7):
    data = pd.DataFrame(data.copy())
    data.set_index('date', inplace=True)

    # добавляем лаги исходного ряда в качестве признаков
    for column in data.columns:
        for i in range(lag_start, lag_end):
            data[f"{column}_t-{i}"] = data[column].shift(i-1)
        if column != target_column:
            data.drop(column, axis=1, inplace=True)

    data["weekday"] = data.index.weekday
    data['is_weekend'] = data.weekday.isin([5, 6]) * 1

    # считаем средние только по тренировочной части, чтобы избежать лика
    data[f'{target_column}_weekday_average'] = data['weekday'].apply(lambda x: weekday_mean_data[x])
    data[f"{target_column}_hour_average"] = hour_average_constant

    # выкидываем закодированные средними признаки
    data.drop(["weekday"], axis=1, inplace=True)

    data = data.dropna()
    data = data.reset_index(drop=True)
    return data


def notebook_prepare_data(all_data, new_data):
    new_data = pd.DataFrame(new_data, index=[0])
    all_data: pd.DataFrame = pd.concat([all_data, new_data], axis=0)
    all_data.set_index(np.arange(len(all_data)), inplace=True)
    if all_data.shape[0] >= 6:
        data = prepare_df(all_data)
        all_data.drop(0, inplace=True)
        return all_data, data
    return all_data, None


class LGBMModel(Model):

    def __init__(self, path_to_weights, config, prepare_data_function=notebook_prepare_data):
        self.path_to_weights = path_to_weights
        self.config = config
        self.booster: Booster = None
        self.all_data = pd.DataFrame()
        self.prepare_data = prepare_data_function

    def predict(self, data):
        logger.debug(f'Got {data}')
        self.all_data, data = self.prepare_data(self.all_data, data)
        logger.debug(f'Modified {self.all_data}')
        if data is not None:
            logger.debug(f'')
            prediction = self.booster.predict(data.values)
            logger.debug(f'Predicted {prediction}')
            return np.exp(prediction)[0]
        return 0

    def load(self):
        self.booster = Booster(model_file=self.path_to_weights)
