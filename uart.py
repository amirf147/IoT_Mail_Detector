#!/usr/bin/env python

from serial_protocol import SerialProtocol
from errors import *
import serial
import time

class Uart(SerialProtocol):
    def __init__(self):
        super().__init__()
        self._port = None
        self._baudrate = None
        self.timeout = 0.1
        self.link = None
        self._command = b'check'
        self._toggle_on = b'on'
        self._toggle_off = b'off'
        

    @property
    def baudrate(self):
        return self._baudrate

    @baudrate.setter
    def baudrate(self, value):
        acceptable_baudrates = (300, 600, 1200, 2400, 4800, 9600, 14400,
                                19200, 28800, 31250, 38400, 57600, 115200,
                                230400, 250000, 500000)
        if not isinstance(value, int):
            raise NotInteger("baudrate must be an integer")
        elif value in acceptable_baudrates:
            self._baudrate = value
        else:
            raise ImproperChoice(f'baudrate must be one of: {acceptable_baudrates}')

    @baudrate.deleter
    def port(self):
        old_baudrate = self._baudrate
        self._baudrate = None
        print(f'old value of host: {old_baudrate} DELETED')

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if value == "/dev/ttyACM0" or value == "/dev/ttyACM1":
            self._port = value
        else:
            raise ImproperChoice("port must ='/dev/ttyACM0' or '/dev/ttyACM1'")

    @port.deleter
    def port(self):
        old_port = self._port
        self._port = None
        print(f'old value of host: {old_port} DELETED')

    def serial_init(self):
        self.link = serial.Serial(self._port, self._baudrate, timeout = self.timeout)

    def get_measurement(self):
        attempts = 0
        with self.link as arduino:
            if arduino.isOpen():
                #time.sleep(1)
                arduino.flush()
                #time.sleep(0.2)
                arduino.write(self._command)
                print('sent check')
                time.sleep(0.2)
                while not arduino.inWaiting():
                    attempts += 1
                    arduino.flush()
                    time.sleep(0.1)
                    arduino.write(self._command)
                else:
                    print(f'attempts needed: {attempts}')
                    data_length = arduino.inWaiting()
                    brightness = arduino.read(data_length).decode().strip()
                    print(brightness)
                    return brightness
    
    def led_on(self):
        with self.link as arduino:
            if arduino.isOpen():
                time.sleep(1)
                print("Connected to arduino")
                arduino.flush()
                arduino.write(self._toggle_on)
                arduino.flush()
                time.sleep(1)
                print('sent on')
                
    def led_off(self):
        with self.link as arduino:
            if arduino.isOpen():
                time.sleep(1)
                print("Connected to arduino")
                arduino.flush()
                arduino.write(self._toggle_off)
                arduino.flush()
                time.sleep(1)
                print('sent off')
