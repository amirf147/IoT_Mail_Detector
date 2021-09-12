#!/usr/bin/env python
#%%
from database import Database
from influxdb import InfluxDBClient

class Influx(Database):

    def __init__(self, username = 'admin', password = 'admin'):
        super().__init__()
        self.db_name = None
        self._username = username
        self._password = password
        self.client = None

    def init_client(self):
        self.client = InfluxDBClient(self._host, self._port, self._username,
                                    self._password, self.db_name)
        
    def send_measurement(self, sensor, measurement):
        try:
            return self.client.write(f'{self.db_name} {sensor}=' + 
                                     f'{str(measurement)}',
                                    {'db': self.db_name}, 204, 'line')
        except Exception:
            print('Make sure <Influx object>.db_name exists as database')
            raise


# %%
