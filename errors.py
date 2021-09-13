#!/usr/bin/env python

"""errors.py: Custom exceptions for property setting """

from sys import exit

if __name__ == "__main__":
    print("I prefer to be a module.")
    exit()

#-----------------------------------------------#
# PROPERTY SETTER ERRORS                        #
#-----------------------------------------------#
class PropertyError(Exception):

    '''Base class of the different property errors'''
    
    __property_error = "Property Setting Error"

    def __init__(self, msg = __property_error):
        self._msg = msg

class ImproperChoice(PropertyError):
    def __init__(self, msg):
        super().__init__()
        self.__msg = msg

    def __str__(self):
        return f'{self._msg} -> {self.__msg}'

class FormatError(PropertyError):
    def __init__(self, msg):
        super().__init__()
        self.__msg = msg

    def __str__(self):
        return f'{self._msg} -> {self.__msg}'

class RangeError(PropertyError):
    def __init__(self, msg):
        super().__init__()
        self.__msg = msg

    def __str__(self):
        return f'{self._msg} -> {self.__msg}'

class NotInteger(PropertyError):
    def __init__(self, msg):
        super().__init__()
        self.__msg = msg

    def __str__(self):
        return f'{self._msg} -> {self.__msg}'

class NotString(PropertyError):
    def __init__(self, msg):
        super().__init__()
        self.__msg = msg

    def __str__(self):
        return f'{self._msg} -> {self.__msg}'
