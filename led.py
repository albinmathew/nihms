import RPi.GPIO as GPIO  
import time  

 
def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(1)  
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(.2)  
        return  

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  
GPIO.setup(22, GPIO.OUT)  
  
for i in range(0,100):
    
    blink(22)
        
GPIO.cleanup()  
