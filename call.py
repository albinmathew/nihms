# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 10:44:46 2014

@author: Albin
"""

import serial
import time
import sys

number="9447541672"

def close():
    ser.close()
    sys.exit() 

def command(msg, timeout=2, ok='OK', end=13, length=100):
    
    t0 = time.time()
    while True:
        ser.write(msg+chr(end))
        
        ret = ser.read(length)
        
        if ok in ret:
            return ret
            
        if time.time()-t0 >= timeout:
                print "Error while executing command "+msg
                close()
                
if __name__ == '__main__':
    
    ser = serial.Serial('/dev/ttyAMA0',9600, rtscts=True, timeout=1)
    ser.open()
    
    command('AT')
    command('ATD'+number+'')
    print "Calling......"
    ser.close()
