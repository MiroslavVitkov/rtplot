#!/bin/python

"""Business logic objects.

"""

import plot
import data
import converter as conv


class MainManager(object):
    def __init__(self):
        # Record new temperatures here
        self.y = []

        # Plots that depend on streamed data
        self.p = plot.Manager(x_axis=range(0, 60))

    def handle_incoming_measurement(self, measurement):
        y = conv.temp2pixels(temp=measurement,
                             temp_range=(-20, 50),
                             graph_height=480)
        self.p.add_point(y)

    def handle_new_dataset(self):
        self.p.clear()

def main():
    m = MainManager()
    for i in range(1, 10):
        for j in range(0, 60):
            m.handle_incoming_measurement(j / float(i))
        m.handle_new_dataset()

if __name__ == "__main__":
    main()
