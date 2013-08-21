#!/bin/python

"""Device -> hw_comm -> dispatch -> parse_com -> convert -> plot
                                 -> log

Update minute, hour and day plots every second.
Update week, month and year plots every day.

"""

import dummy_device as dev
import plot
import data
import converter as conv


DATAPOINTS_PER_GRAPH = 60


class MainManager(object):
    def __init__(self):
        # Initialize device communication
        self.s = dev.Simple(clb=self.handle_incoming_measurement)

        # Record new temperatures here
        self.l = data.Logger

        # Plots that depend on streamed data
        self.p = plot.Manager(x_axis=conv.get_axis(DATAPOINTS_PER_GRAPH))

    def handle_incoming_measurement(self, measurement):
        # Log
        self.l.add_line(measurement)

        # Draw
        self.p.add_point(measurement - conv.MIN_TEMP)  # scale [0, TEMP_RANGE]

    def handle_new_dataset(self):
        self.p.clear()

def main():
    if 0:
        m = MainManager()
        for i in range(1, 10):
            for j in range(0, 60):
                m.handle_incoming_measurement(j / float(i))
            m.handle_new_dataset()

    if 1:
        m = MainManager()
        m.s.run()

if __name__ == "__main__":
    main()
