#!/usr/bin/env python
#%%
from errors import *
from sense_hat import SenseHat

class Sensor:
    def __init__(self, sensor = None, board = None):
        self.sensor = sensor
        self._board = board
        self.measurement = {}

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        value = value.lower()
        if value == 'raspberry' or value == 'arduino':
            self._board = value
        elif value == 'sensehat':
            self._board = value
        else:
            raise ImproperChoice("board must be 'raspberry' or 'arduino'" +
                                 "or 'sensehat'")

    @board.deleter
    def board(self):
        old_board = self._board
        self._board = None
        print(f'old value of host: {old_board} DELETED')

    def measure(self):
        if self.sensor == 'temperature':
            self.measurement = SenseHat().temp
            return self.measurement
        elif self.sensor == 'pressure':
            self.measurement = SenseHat().pressure
            return self.measurement
        elif self.sensor == 'humidity':
            self.measurement = SenseHat().humidity
            return self.measurement
        elif self.sensor == 'accelerometer':
            self.measurement = SenseHat().get_accelerometer_raw()
            return self.measurement
        else:
            raise ImproperChoice('when getting sensehat measurement, sensor' +
                                 'must be named either "temperature",' +
                                 '"pressure" or "humidity"')

# %%
