#!/usr/bin/env python

from setup import sensor_measurements, messages, accelerometer, poll_sensors, influx, API_KEY
from datetime import datetime
import picamera
import time
import telegram
#from telegram.ext import *
import threading
import requests
import serial as ser
import actions

def measurement_loop() -> None:
    
    received = 1 # used as datapoint to indicate received mail in the database
    bot = telegram.Bot(API_KEY)
    start_time, mail_time = datetime.now()

    while True:
        time_now = datetime.now()

        #continuosly update accelerometer readings
        mail_slot_opened = actions.mail_slot_check(accelerometer.measure())
        print(mail_slot_opened)
        
        diff = time_now - start_time #how much time elapsed since last poll
        mail_diff = time_now - mail_time #time between mail reception

        global sensor_measurements
        sensor_measurements = poll_sensors() # get sensor measurements
        print(sensor_measurements)

        if int(sensor_measurements['brightness']) > 40:
            requests.get(messages['door_open'])

        if diff.seconds >= 5:
            #sensor measurements has to be global because it is being
            #used in the the telegram thread and the sensor updated
            #values need to be accessible from there for any queries
            global sensor_measurements
            sensor_measurements = poll_sensors() # get sensor measurements
            print(sensor_measurements)
            
            #check for door open condition
            if int(sensor_measurements['brightness']) > 10:
                requests.get(messages['door_open'])

            # Send the sensor data to the database
            for sensor, measurement in sensor_measurements.items():
                print(f'sensor: {sensor} measurement: {measurement}')
                influx.send_measurement(sensor, measurement)

            start_time = datetime.now() #reset time tracker

        if mail_slot_opened and mail_diff.seconds > 3:
            
            requests.get(messages['mail_rx'])
            a = ser.Serial("/dev/ttyACM0", 500000, timeout=0.1)
            counter = 0
            while a.isOpen() and counter < 5:
                print("{} connected!".format(a.port))
                time.sleep(0.2)
                a.write(b'on')
                time.sleep(0.2)
                counter += 1
                
            influx.send_measurement('mail', received) #update mail tracker in db
            print("\nTaking picture")
            with picamera.PiCamera() as camera:
                camera.resolution = (1280, 720)
                date = datetime.now()
                path = "/home/pi/pipics/" + str(date) + ".jpg"

                camera.capture(path)
                bot.send_document(1734914451, open(path, 'rb'))
                print("\nPicture taken")

            mail_time = datetime.now()

            a = ser.Serial("/dev/ttyACM0", 500000, timeout=0.1)
            counter2 = 0
            while a.isOpen() and counter2 < 5:
                print("{} connected!".format(a.port))
                time.sleep(0.2)
                a.write(b'off')
                time.sleep(0.2)
                counter2 += 1
                        
if __name__ == 'main':
    t2 = threading.Thread(target = measurement_loop)
    #t1.start()
    t2.start()