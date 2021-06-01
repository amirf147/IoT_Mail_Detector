from influx import *
from uart import Uart
from sensor import *
from telegram_bot import *
import picamera
import threading

# Database client set up
influx = Influx()
influx.host = 'localhost'
influx.port = 8086
influx.db_name = 'testing'
influx.init_client()
client = influx.client

# Serial communication set up
serial = Uart()
serial.baudrate = 500000
serial.port = "/dev/ttyACM0"
serial.serial_init()



# Sensors on Arduino set up
brightness = Sensor('photoresistor', 'arduino')

# Sensors on SenseHat set up
temperature = Sensor('temperature', 'sensehat')
pressure = Sensor('pressure', 'sensehat')
humidity = Sensor('humidity', 'sensehat')
accelerometer = Sensor('accelerometer', 'sensehat')

def poll_sensors():
     return {'brightness'    : serial.get_measurement(),
             'temperature'   : round(float(temperature.measure()), 2),
             'pressure'      : round(float(pressure.measure()), 2),
             'humidity'      : round(float(humidity.measure()), 2),
             }

sensors = poll_sensors() #init global variable with values

# Telegram bot setup into thread
def bot_listener():
    global sensors
    telebot = TelegramBot(sensors)
    telebot.dispatcher.add_handler(CommandHandler("start", telebot.start_command))
    telebot.dispatcher.add_handler(CommandHandler("help", telebot.help_command))
    telebot.dispatcher.add_handler(MessageHandler(Filters.text, telebot.handle_message))
    telebot.dispatcher.add_error_handler(telebot.error)
    telebot.updater.start_polling()
    telebot.updater.idle()

t1 = threading.Thread(target = bot_listener)
t1.start()