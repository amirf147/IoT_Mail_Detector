#!/usr/bin/env python

from setup import *
from datetime import datetime
import time

received = 1 # used as signal to indicate received mail
#%%
def mail_slot_check(accel):
    if accel['z'] > 0.30:
        return True
    else:
        return False
#%%
def poll_sensors():
     return {'brightness'    : serial.get_measurement(),
             'temperature'   : temperature.measure(),
             'pressure'      : pressure.measure(),
             'humidity'      : humidity.measure(),
             }

def measurement_loop():

    start_time = datetime.now()

    while True:

        time_now = datetime.now()

        #continuosly update accelerometer readings
        mail_slot_opened = mail_slot_check(accelerometer.measure())
        print(mail_slot_opened)
        
        
        diff = time_now - start_time #how much time elapsed since last poll

        if diff.seconds >= 5:

            sensors = poll_sensors() # get sensor measurements
            print(sensors)

            # Send the sensor data to the database
            for sensor, measurement in sensors.items():
                print(f'sensor: {sensor} measurement: {measurement}')
                influx.send_measurement(sensor, measurement)

            start_time = datetime.now() #reset time tracker

        if mail_slot_opened:
            print('tilt')
            influx.send_measurement('mail', received) #update mail tracker in db

# main loop
measurement_loop()