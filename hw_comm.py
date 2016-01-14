#!/usr/bin/env python

"""Receive line strings from device. Parse them and return numeric temperatures.

"""

import serial
import string
import sys
import time

MAX_TEMP = 60
MIN_TEMP = 10
NEWLINE = "\n"

class Serial(object):
    """Serial duplex communication."""
    def __init__(self, simulate=False):
        self.simulate = simulate
        if not simulate:
            self.comm = serial.Serial(port='/dev/ttyUSB0',
                                      baudrate=38400,
                                      bytesize=serial.EIGHTBITS,
                                      parity=serial.PARITY_NONE,
                                      stopbits=serial.STOPBITS_ONE,
                                      timeout=None,
                                      xonxoff=False,
                                      rtscts=False,
                                      writeTimeout=None,
                                      dsrdtr=False,
                                      interCharTimeout=None,
                                      )

    def run(self):
        if self.simulate:
            self._generate_random_data()
        else:
            self._listen_forever()

    def _listen_forever(self):
        """Blocking! Forever!"""
        def rl(size=None, eol=NEWLINE):
            """pyserial's implementation does not support the eol parameter"""
            ret = ""
            while True:
                x = self.comm.read()
                ret = ret + x
                if x == eol:
                    return ret
        self.comm.readline = rl
        while True:
            measurement = self.comm.readline()
            temp = self._parse_line_return_temp(measurement)
            if temp is not None:
                print x

    def _generate_random_data(self):
        """For debug purposes."""
        import random
        while True:
            measurement = str(random.randint(MIN_TEMP, MAX_TEMP)) + ".0"
            print measurement
            time.sleep(0.3)

    def _parse_line_return_temp(self, line):
        try:
            s1 = string.split(s=line, sep=' ')  # time decicelsius
            return (float(s1[1]) / 10 )
        except ValueError:
            return None


def main():
    comm = Serial(simulate=False)
    comm.run()

if __name__ == "__main__":
    main()
