#!/usr/bin/env python
#%%
import errors as err
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
        if not isinstance(value, str):
            raise err.NotString('value must be a string')
        value = value.lower()
        if value not in ['raspberry, arduino, senshat']:
            raise err.ImproperChoice("board must be 'raspberry', arduino'" +
                                      "or 'sensehat'")
        self._board = value
            
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
            raise err.ImproperChoice('when getting sensehat measurement, sensor' +
                                     'must be named either "temperature",' +
                                     '"pressure" or "humidity"')

# %%
