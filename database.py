#!/usr/bin/env python

"""database.py: Database class for creating database objects"""

from sys import exit
from errors import *

if __name__ == "__main__":
    print("I prefer to be a module.")
    exit()

class Database:

    def __init__(self):
        self._type = None
        self._host = None
        self._port = None
    
    def __str__(self): 
        # when printing the class instance
        return 'Database class with __dict__: ' + str(self.__dict__)

    #-----------------------------------------------#
    # TYPE getter/setter/deleter                    #
    #-----------------------------------------------#
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, entered):
        entered = entered.lower()
        types = ['local', 'remote', 'cloud']
        if entered not in types:
            raise ImproperChoice("type must be either local, remote or cloud")
        else:
            self._type = entered
    
    @type.deleter
    def type(self):
        old_type = self._type
        self._type = None
        print(f'old value of host: {old_type} DELETED')

    #-----------------------------------------------#
    # HOST getter/setter/deleter                    #
    #-----------------------------------------------#
    @property
    def host(self):
        return self._host
        
    @host.setter
    def host(self, ip):
        split_ip = ip.split(".")
        if ip == 'localhost':
            self._host = ip
        elif len(split_ip) < 4 or len(split_ip) > 4:
            raise FormatError("Not in form 'x.x.x.x'")
        else:
            for octet in split_ip:
                if int(octet) > 0 and int(octet) <= 255:
                    pass
                else:
                    raise RangeError("1 or more octets out of range")
        self._host = ip

    @host.deleter
    def host(self):
        old_host = self._host
        self._host = None
        print(f'old value of host: {old_host} DELETED')

    #-----------------------------------------------#
    # PORT getter/setter/deleter                    #
    #-----------------------------------------------#
    @property
    def port(self):
        return self._port
    
    @port.setter
    def port(self, entered):
        warning = RangeWarning('port is in registered range: ' +
                               'make sure its not being used')
        if not isinstance(entered, int):
            raise NotInteger("port must be an integer")
        elif entered >= 0 and entered < 1024:
            raise RangeError("Port is in the well-known range, port not set")
        elif entered >= 1024 and entered < 49152:
            try:
                raise warning
            except:
                print(warning.__class__.__name__, warning)
            finally:
                self._port = entered
        elif entered >= 49152 and entered < 65536:
            self._port = entered
        else:
            raise RangeError('port is out of range, port not set')     
            
    @port.deleter
    def port(self):
        old_port = self._port
        self._port = None
        print(f'old value of host: {old_port} DELETED')
