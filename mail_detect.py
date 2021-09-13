#!/usr/bin/env python

from setup import sensors, messages, accelerometer, poll_sensors, influx, picamera, API_KEY
from datetime import datetime
import time
import telegram
#from telegram.ext import *
import threading
import requests
import serial as ser
import actions

#import logging


# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

received = 1 # used as signal to indicate received mail


# def mail_slot_check(accel):
#     if accel['y'] > .3:
#         return True
#     else:
#         return False

# def poll_sensors():
#      return {'brightness'    : serial.get_measurement(),
#              'temperature'   : round(float(temperature.measure()), 2),
#              'pressure'      : round(float(pressure.measure()), 2),
#              'humidity'      : round(float(humidity.measure()), 2),
#              }

# sensors = poll_sensors() #init global variable with values

# def telegram_loop():
    
#     def responses(query):
#         global sensors
#         query = query.lower()
    
#         if query in ('temp', 'temperature', 't'):
#             reading = sensors['temperature']
#             resp = f'{reading} degrees Celsius'
#             return resp
#         elif query in ('pressure', 'press', 'p'):
#             reading = sensors['pressure']
#             resp = f'{reading} millibar'
#             return resp
#         elif query in ('humidity', 'humid', 'h'):
#             reading = sensors['humidity']
#             resp = f'{reading}%'
#             return resp
#         elif query in ('brightness', 'bright', 'b'):
#             return sensors['brightness']
#         else:
#             return 'unknown query'

#     def start_command(update, context):
#         update.message.reply_text("I hear you loud and clear!")

#     def help_command(update, context):
#         update.message.reply_text("commands = t, p, h, b")
    
#     def handle_message(update, context):
#         text = str(update.message.text).lower()
#         response = responses(text)
    
#         update.message.reply_text(response)
    
#     def error(update, context):
#         print(f'Update {update} caused error {context.error}')

#     updater = Updater(token= API_KEY, use_context=True)
#     dispatcher = updater.dispatcher
    
#     dispatcher.add_handler(CommandHandler("start", start_command))
#     dispatcher.add_handler(CommandHandler("help", help_command))
#     dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
#     dispatcher.add_error_handler(error)
#     updater.start_polling()
#     updater.idle()


def measurement_loop():
    
    bot = telegram.Bot(API_KEY)
    
    print('loop started')

    start_time = datetime.now()
    mail_time = datetime.now()

    while True:

        time_now = datetime.now()

        #continuosly update accelerometer readings
        mail_slot_opened = actions.mail_slot_check(accelerometer.measure())
        print(mail_slot_opened)
        
        diff = time_now - start_time #how much time elapsed since last poll
        mail_diff = time_now - mail_time #time between mail reception

        global sensors
        sensors = poll_sensors() # get sensor measurements
        print(sensors)
        if int(sensors['brightness']) > 40:
            requests.get(messages['door_open'])

        if diff.seconds >= 5:

            # Send the sensor data to the database
            for sensor, measurement in sensors.items():
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