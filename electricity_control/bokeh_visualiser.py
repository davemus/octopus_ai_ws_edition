# http://bokeh.pydata.org/en/0.11.0/docs/user_guide/server.html
# https://www.youtube.com/watch?v=NUrhOj3DzYs
from typing import Sequence

from bokeh.palettes import Viridis
import json
from loguru import logger

from redis import StrictRedis
from concurrent.futures import ThreadPoolExecutor

from bokeh.util.browser import view

from jinja2 import Environment, FileSystemLoader

from tornado.web import RequestHandler

from bokeh.embed import server_document
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.server.server import Server

env = Environment(loader=FileSystemLoader('templates'))


class BokehVisualiser:

    def __init__(self, redis_url: str, real_data_topic: str, data_interval: str, models_list: Sequence[str],
                 pool_delay: int=2):
        self.redis = StrictRedis.from_url(redis_url)
        self.real_data_topic = real_data_topic
        self.pool_delay = pool_delay
        channels = [f'{model_name}_{data_interval}' for model_name in models_list]
        channels.append(real_data_topic)
        self.channels = channels
        self.x_column = 'date'

        self.source = ColumnDataSource({k: list() for k in self.channels + [self.x_column]})
        self.p = figure(plot_width=950, height=300, tools='')
        for channel, color in zip(self.channels, Viridis[len(channels)]):
            self.p.line(source=self.source, x=self.x_column, y=channel, line_width=2, alpha=.85, color=color)

        self.channel_counters = {k: 0 for k in self.channels}
        self.callbacks_executor = None

    def start(self):
        self.callbacks_executor = ThreadPoolExecutor(max_workers=2)
        self.callbacks_executor.submit(self._job)

    def _job(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.channels)
        for message in pubsub.listen():
            logger.debug(message)
            try:
                if message['type'] != 'message':
                    continue
                self.channel_counters[message['channel']] += 1
                data = json.loads(message['data'])
                if isinstance(data, dict):
                    data = data.get('Global_active_power')
                self.source.stream({message['channel']: [data],
                                    self.x_column: [self.channel_counters[message['channel']]]},
                                   100)
            except Exception as e:
                logger.trace(e)

    def modify_doc(self, doc):
        #doc = curdoc()
        logger.info(f'{doc}, Modifying doc')
        doc.add_root(self.p)


class IndexHandler(RequestHandler):
    def get(self):
        template = env.get_template('embed.html')
        script = server_document('http://localhost:5006/bkapp')
        self.write(template.render(script=script))

# Setting num_procs here means we can't touch the IOLoop before now, we must
# let Server handle that. If you need to explicitly handle IOLoops then you
# will need to use the lower level BaseServer class.


def start_server(*args, **kwargs):
    visualizer = BokehVisualiser(*args, **kwargs)
    visualizer.start()
    server = Server({'/bkapp': visualizer.modify_doc}, num_procs=4, extra_patterns=[('/', IndexHandler)])
    server.start()
    server.io_loop.add_callback(view, "http://localhost:5006/")
    server.io_loop.start()


if __name__ == '__main__':
    start_server(redis_url='redis://redis:6379', real_data_topic='test', data_interval='d', models_list=['lstm', 'lgbm'])

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
