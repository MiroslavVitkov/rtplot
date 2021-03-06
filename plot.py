#!/usr/bin/env python

"""A colelction of classes for dynamically updated XY-plots.

"""

# Constants
MINUTE_S = 60
HOUR_S = MINUTE_S * 60
DAY_S = HOUR_S * 24
WEEK_S = DAY_S * 7
MONTH_S = DAY_S * 30
YEAR_S = DAY_S * 365


# Settings
MAX_TEMP = 60
MIN_TEMP = 0
DATAPOINTS_PER_GRAPH = 60
TIME_INTERVALS = [MINUTE_S,
                  HOUR_S,
#                  DAY_S,
#                  WEEK_S,
#                  MONTH_S,
#                  YEAR_S,
                  ]

# Imports
import matplotlib.pyplot as plt
import collections as col
import numpy as np

class Demuxer(object):
    """Based on input temperature, update plots as needed"""
    def __init__(self):
        self.w = Window()
        self._counter_samples = 0

    def handle_new_value(self, vals):
        """Update relevant plots."""
        self._counter_samples += 1

        # Update shortest interval plot. This always happens.
        self.w.add_datapoint(plot_number=0, y=vals)

        # Calculate the impact of a new point on the averaging plots.
        # We skip the first plot, because it is already covered above.
        for i, v in enumerate(TIME_INTERVALS[:-1]):
            target_plot = i + 1
            if self._counter_samples % v == 0:
                #avv_vals = self._get_average(plot_num = target_plot - 1) # next shorter interval
                self.w.add_datapoint(plot_number=target_plot,
                                     y=vals)  # TODO: use avv_vals

    def _get_average(self, plot_num):  # TODO: vectorize!
        data = self.w.get_yaxis(plot_num=plot_num)
        # np.mean() silently hangs :(
        average = np.mean(data, axis=1)
        return list(average)

class Window(object):
    """Holds a collection of equally-sized, static x-axis, dynamic
     y-axis plots. Temperature range aware. Takes up the whole screen.

    """
    def __init__(self):
        # Redraw plots as soon as self.fig.canvas.draw() is called.
        plt.ion()

        # Create the window surface
        dpi=80  # default value
        screen = get_screen_resolution()
        width = screen[0] / dpi
        height = screen[1] / dpi
        self.fig = plt.figure(figsize=(width, height), dpi=dpi)  # the main window

        # Create the individual plots
        self.plots = []
        plots_map = 100 + len(TIME_INTERVALS) * 10   # 234 means 2x3 grid, 4th subplot
        for i, d in enumerate(TIME_INTERVALS):
            x_axis = np.linspace(0, d, DATAPOINTS_PER_GRAPH)
            graph = Graph(window=self.fig, subplot_num=plots_map + i + 1, x_axis=x_axis)
            self.plots.append(graph)

    # Redrawing belongs here for fine control over this time-consuming operation.
    # Note that fig.canvas.draw() redraws the whole window!
    def add_datapoint(self, plot_number, y):
        self.plots[plot_number].add_datapoint(y)
        self.fig.canvas.draw()

    def get_yaxis(self, plot_num):
        return self.plots[plot_num].y_data


class Graph(object):
    # Datapoints 'y' can contain arbitrary number of elements.
    # Each index in 'y' is treated as separate signal.
    # Signal hystory is kept as list of deques.
    # Each deque represents1 a circular buffer of a single signal.
    def __init__(self, window, subplot_num, x_axis, dim=2):
        ax = window.add_subplot(subplot_num)
        l = len(x_axis)
        self.y = ax.plot(range(l), l*[-1,], '-',       # Obtain handle to y axis.
                         range(l), l*[-1,], '--',
                         marker='^'
                         )
        # Hack: because initially the graph has too few y points, compared to x points,
        # nothing should be shown on the graph.
        # The hack is that initial y axis is seto be be below in hell.
        self.y_data = []
        for i in range(dim):
            self.y_data.append( col.deque(len(x_axis)*[-9999,],          # Circular buffer.
                                          maxlen=len(x_axis)
                                          )
                              )

        # Make plot prettier
        plt.grid(True)
        plt.tight_layout()
        ax.set_ylim(MIN_TEMP, MAX_TEMP)
        plt.figlegend(self.y, ('tempr', 'ctrl'), 'upper right');
        ax.set_ylabel('temperature [C]')
        # Terrible hack!
        if subplot_num == 121:
            ax.set_xlabel('time [s]')
        else:
            ax.set_xlabel('time [min]')

    def add_datapoint(self, y):
        if not isinstance(y, col.Sequence):
            y = [y,]

        for i in range( len(y) ):
            self.y_data[i].appendleft(y[i])
            self.y[i].set_ydata( self.y_data[i] )


def get_screen_resolution():
    return 1366, 768


def main():
    import sys
    d = Demuxer()
    while True:
        # Plot space delimited line of measurements.
        try:
            line = sys.stdin.readline()
            values = line.split()
            cast = (values[1], values[2])
            d.handle_new_value(cast)
        except:
            pass


if __name__ == "__main__":
    main()
