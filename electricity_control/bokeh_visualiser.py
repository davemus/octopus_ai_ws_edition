# http://bokeh.pydata.org/en/0.11.0/docs/user_guide/server.html
# https://www.youtube.com/watch?v=NUrhOj3DzYs

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

from bokeh.transform import factor_cmap
from bokeh.layouts import gridplot

import os
import numpy as np
import pandas as pd
import random

from statsmodels.tsa.api import Holt


class BokehVisualiser:

    def __init__(self):
        pass


# data_file_path = os.path.join(os.path.dirname(__file__), 'data', 'data_temp_pow_fan.csv')
# df = pd.read_csv(data_file_path, parse_dates=['dt'])
#
# source = ColumnDataSource(dict(x=[], x_pred=[], temp=[], power=[], fan=[], frcst=[]))
#
# plot_options = dict(plot_width=950, height=300, tools='')
#
# s1 = Figure(title='Temperature of CPU', **plot_options)
# s1.line(source=source, x='x', y='temp', line_width=2, alpha=.85, color='red', legend='Temperature, C')
#
# s1.line(source=source, x='x_pred', y='frcst', line_width=2, alpha=.85, color='green', legend='Forecasted temp., C ')
#
# s2 = Figure(x_range=s1.x_range, title='Power on CPU unit', **plot_options)
# s2.line(source=source, x='x', y='power', line_width=2, alpha=.85, color='orange', legend='Power, W')
#
# s3 = Figure(x_range=s1.x_range, title='Fan rotation speed', **plot_options)
# s3.line(source=source, x='x', y='fan', line_width=2, alpha=.85, color='blue', legend='Speed, RPM')
#
# p = gridplot([[s1], [s2], [s3]])
#
# temp = 0
# power = 0
# ind = 0
# fan = 0
#
#
# def update_data():
#     global ind, power, temp
#     ind += 1
#     temp = df.loc[ind, 'CPU_temperature']
#     power = df.loc[ind, 'CPU_power']
#     fan = df.loc[ind, 'cooler_RPM']
#
#     model = Holt(df.loc[(ind - 20):ind, 'CPU_temperature'].tail(10).values)
#     model.fit()
#     p = model.params
#     frcst = model.predict(params=p, start=5, end=5)
#     p = ind + 5
#
#     new_data = dict(x=[ind], temp=[temp], power=[power], x_pred=[p], fan=[fan], frcst=[frcst])
#     source.stream(new_data, 100)
#
#
# curdoc().add_root(p)
# curdoc().add_periodic_callback(update_data, 500)
