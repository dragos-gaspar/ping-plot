import logging
import warnings

import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import DateFormatter

from config import Config

# Workaround for issue where main thread hands on plt.show() after closing plot window
matplotlib.use('WxAgg')

warnings.filterwarnings("ignore")
logger = logging.getLogger('ping-plot')


class Plotter:
    def __init__(self, frame):
        self.frame = frame

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.formatter = DateFormatter('%H:%M:%S')

    def _plot_frame(self, _) -> None:
        """
        Method that generates a plot view. Should be
        passed as argument to `matplotlib.animation.FuncAnimate`.

        :param _: Current frame; not used.
        """
        self.ax.clear()
        timestamps, data = self.frame()
        self.ax.plot(timestamps, data)

        plt.subplots_adjust(bottom=0.2)

        plt.xlabel("Time [h:m:s]")
        plt.ylabel("Ping [ms]")

        plt.xticks(rotation=45, ha='right')
        self.ax.xaxis.set_major_formatter(self.formatter)

    def plot(self) -> None:
        _ = FuncAnimation(self.fig, self._plot_frame, interval=Config.PLOT_REFRESH_RATE * 1000)
        logger.debug('Showing plot window...')
        plt.show()
