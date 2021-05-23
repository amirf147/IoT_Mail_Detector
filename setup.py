from influx import *
from uart import Uart
from sensor import *
import picamera

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

