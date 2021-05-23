#!/usr/bin/env python
#%%
from errors import *

class SerialProtocol:
    def __init__(self):
        self.main = None
        self.secondary = None
        self._protocol = None
        self._clockrate = None

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        value = value.lower()
        if value in ['i2c', 'spi', 'uart']:
            self._protocol = value
        else:
            raise ImproperChoice("protocol must be 'raspberry' or 'arduino'")

    @protocol.deleter
    def protocol(self):
        old_protocol = self._protocol
        self._protocol = None
        print(f'old value of host: {old_protocol} DELETED')