#!/usr/bin/env python

"""database.py: Database class for creating database objects"""
#%%
from sys import exit
import errors as err
import warnings

if __name__ == "__main__":
    print("I prefer to be a module.")
    exit()

class Database:

    def __init__(self):
        self._db_type = None
        self._host = None
        self._port = None
    
    def __str__(self): 
        # when printing the class instance
        return 'Database class with __dict__: ' + str(self.__dict__)

    #-----------------------------------------------#
    # TYPE getter/setter/deleter                    #
    #-----------------------------------------------#

    @property
    def db_type(self):
        return self._db_type
    
    @db_type.setter
    def db_type(self, entered):
        if not isinstance(entered, str):
            raise err.NotString('db_type must string')
        types = ['local', 'remote', 'cloud']
        if entered.lower() not in types:
            raise err.ImproperChoice("db_type must be either local, remote or cloud")
        else:
            self._db_type = entered
    
    @db_type.deleter
    def db_type(self):
        old_type = self._db_type
        self._db_type = None
        print(f'old value of host: {old_type} DELETED')

    #-----------------------------------------------#
    # HOST getter/setter/deleter                    #
    #-----------------------------------------------#
    @property
    def host(self):
        return self._host

    def octet_check_failed(self, split_ip):
        for octet in split_ip:
            if not (int(octet) > 0 and int(octet) <= 255):
                return True
        return False
                
    @host.setter
    def host(self, ip):
        if not isinstance(ip, str):
            raise err.NotString('db_type must be string')
        split_ip = ip.split(".")
        if ip.lower() == 'localhost':
            self._host = ip
        elif len(split_ip) < 4 or len(split_ip) > 4:
            print(len(split_ip))
            raise err.FormatError("Not in form 'x.x.x.x' or 'localhost'")
        elif self.octet_check_failed(split_ip):
            raise err.RangeError("1 or more octets out of range")
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
        if not isinstance(entered, int):
            raise err.NotInteger("port must be an integer")
        elif entered >= 0 and entered < 1024:
            raise err.RangeError("Port is in the well-known range, port not set")
        elif entered >= 1024 and entered < 49152:
            warnings.warn('port is in registered range.' + 
                          'Make sure its not being used')
            self._port = entered
        elif entered >= 49152 and entered < 65536:
            self._port = entered
        else:
            raise err.RangeError('port is out of range, port not set')     
            
    @port.deleter
    def port(self): 
        old_port = self._port
        self._port = None
        print(f'old value of host: {old_port} DELETED')

# %%
