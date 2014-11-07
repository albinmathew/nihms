import RPi.GPIO as GPIO  
import time  
 
 
def blink():
        
        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)  
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(23, GPIO.OUT)
        
        for i in range(0,100):
                
                GPIO.output(22,GPIO.HIGH)
                GPIO.output(23,GPIO.LOW)
                time.sleep(.5)
                GPIO.output(22,GPIO.LOW)
                GPIO.output(23,GPIO.HIGH)
                time.sleep(.5)
	GPIO.cleanup()
        return

GPIO.setwarnings(False)

blink()  
   
        
  
