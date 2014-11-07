# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 23:05:57 2014

@author: Albin
"""
import serial
import time
import sys

number="9447541672"
message="Python serial program test GSM"

def sms():
    global ser
    ser = serial.Serial('/dev/ttyAMA0',9600, rtscts=True, timeout=1)
    ser.open()
    
    command('AT+CMGF=1')
    command('AT+CMGS="'+number+'"', ok='>')
    command(message, end=26, timeout=10)
    time.sleep(.1)
    print "Message sent succesfully"
    ser.close()

def close():
    ser.close()
    sys.exit() 

def command(msg, timeout=2, ok='OK', end=13, length=100):
    
    t0 = time.time()
    while True:
        ser.write(msg+chr(end))
        time.sleep(.5)
        ret = ser.read(length)
        
        if ok in ret:
            return ret
            
        if time.time()-t0 >= timeout:
                print "Error while executing command "+msg
                close()
                
if __name__ == '__main__':
    
   sms()
