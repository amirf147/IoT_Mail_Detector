#!/usr/bin/env python

"""errors.py: Contains error messages that might arise in creating objects"""

from sys import exit

if __name__ == "__main__":
    print("I prefer to be a module.")
    exit()

#-----------------------------------------------#
# PROPERTY SETTER ERRORS                        #
#-----------------------------------------------#
class PropertyError(Exception):
    
    _property_error = "<<<ERROR in creating property!>>>"

    def __init__(self, msg = _property_error):
        self.msg = msg

class ImproperChoice(PropertyError):
    def __init__(self, msg):
        super().__init__()
        print(self.msg)

class FormatError(PropertyError):
    def __init__(self, msg):
        super().__init__()
        print(self.msg)

class RangeError(PropertyError):
    def __init__(self, msg):
        super().__init__()
        print(self.msg)

class NotInteger(PropertyError):
    def __init__(self, msg):
        super().__init__()
        print(self.msg)

#-----------------------------------------------#
# PROPERTY SETTER WARNINGS                      #
#-----------------------------------------------#
class PropertyWarning(Exception):

    _property_warning = "<<<WARNING in creating property!>>>"

    def __init__(self, msg = _property_warning):
        self.msg = msg

class RangeWarning(PropertyWarning):
    def __init__(self, msg):
        super().__init__()
        print(self.msg)
