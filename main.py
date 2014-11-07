import nihms
from sms import *
import sys,serial,numpy,subprocess
from PyQt4 import QtCore,QtGui
import PyQt4.Qwt5 as Qwt
import numpy, scipy, pylab
import RPi.GPIO as GPIO


    
class EasyPulse:
    
        def __init__(self, debug=0, pin_epulse=6):
                self.DEBUG = debug

                GPIO.setmode(GPIO.BCM)
                GPIO.setwarnings(False)

                self.SPICLK = 11
                self.SPIMISO = 9
                self.SPIMOSI = 10
                self.SPICS = 8

                GPIO.setup(self.SPIMOSI, GPIO.OUT)
                GPIO.setup(self.SPIMISO, GPIO.IN)
                GPIO.setup(self.SPICLK, GPIO.OUT)
                GPIO.setup(self.SPICS, GPIO.OUT)

                self.PIN_EPULSE = pin_epulse

       
        def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
                global adcout
                try:
                        if ((adcnum > 7) or (adcnum < 0)):
                                return -1
                        GPIO.output(cspin, True)
                        GPIO.output(clockpin, False)  
                        GPIO.output(cspin, False)    

                        commandout = adcnum
                        commandout |= 0x18  
                        commandout <<= 3    
                        for i in range(5):
                                if (commandout & 0x80):
                                        GPIO.output(mosipin, True)
                                else:
                                        GPIO.output(mosipin, False)
                                commandout <<= 1
                                GPIO.output(clockpin, True)
                                GPIO.output(clockpin, False)

                        adcout = 0
                      
                        for i in range(12):
                                GPIO.output(clockpin, True)
                                GPIO.output(clockpin, False)
                                adcout <<= 1
                                if (GPIO.input(misopin)):
                                        adcout |= 0x1
        
                        GPIO.output(cspin, True)

                        adcout /= 2     

                except:
                        adcout = 0

                return adcout

        def computeHeartrate(self, beats):
            
                global heartrate
                intervals = []
                for i in range(1, len(beats)):
                        intervals.append(beats[i]-beats[i-1])

                if len(intervals) < 3:
                        heartrate = -1
                else:
                    
                        intervals.sort()
                        intervals.pop(0)
                        intervals.pop(len(intervals)-1)

                        average_interval = sum(intervals) / len(intervals)
                        heartrate = round(60 / average_interval, 2)

                return heartrate

        def readPulse(self):
                THRESHOLD=1010
                READING_INTERVAL = 0.1
                READ_FOR_SECONDS = 5
                CURRENT_READING_TIME = 0
                beats = []
                pulse = False

                if self.DEBUG:
                        print ("Total reading time will be " + str(READ_FOR_SECONDS) + "s")
        
                while CURRENT_READING_TIME < READ_FOR_SECONDS:
                        reading = self.readadc(self.PIN_EPULSE, self.SPICLK, self.SPIMOSI, self.SPIMISO, self.SPICS)

                        for i in range(int(reading / 100)):
                                if self.DEBUG:
                                        print( ".",)

                        if (reading > THRESHOLD):
                                if not pulse:
                                        pulse = True
                                        if self.DEBUG:
                                                print ("Beat")
                                        beats.append(CURRENT_READING_TIME)
                                else:
                                        if self.DEBUG:
                                                print ("")
                        else:
                                pulse = False
                                if self.DEBUG:
                                        print ("")

                        time.sleep(READING_INTERVAL)
                        CURRENT_READING_TIME = CURRENT_READING_TIME + READING_INTERVAL
                        if self.DEBUG:
                                print( "Current reading time is " + str(CURRENT_READING_TIME))

                return beats
            
    
def plot():
    
    global y
    c.setData(x,y)
    y=numpy.roll(y,-1)
    uiplot.plot.replot()

def start():
    
        global signal
        global heartrate
        global spo2
        
        easypulse = EasyPulse()
        beats = easypulse.readPulse()
        heartrate = easypulse.computeHeartrate(beats)
        spo2 = spo2()
        
        #print ("Number of beats: " + str(len(beats)))
        #print( "Heartrate: " + str(heartrate))
        
        signal=[]
        
        for i in range(1,100):
            
            reading = easypulse.readadc(2, 11, 10, 9, 8)
            signal.append(reading*3.3/1023)
            
        fft=scipy.fft(signal)
        bp=fft[:]
        
        for i in range(len(bp)): 
         if i>=10:bp[i]=0  

        ibp=scipy.ifft(bp)
        


def spo2():
            
        global spo2
        #easypulse = EasyPulse()
            
        red=[10,23,52,4,8,92]
        ir=[1,8,97,85,96,15]
        """    
        for i in range(1,100):
                    
                ch0 = easypulse.readadc(0, 11, 10, 9, 8)
                ch2 = easypulse.readadc(2, 11, 10, 9, 8)
                    
                red.append(ch0*3.3/1023)
                ir.append(ch2*3.3/1023)
        """            
        spo2 = round(max(red)/max(ir), 2)

        return spo2           
                         
    

if __name__== "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    win_plot = nihms.QtGui.QWidget()
    uiplot = nihms.Ui_Form()
    uiplot.setupUi(win_plot)
    start()
    uiplot.lcdNumber.display(heartrate)
    uiplot.lcdNumber_2.display(spo2)
  
    
    n=1000
    x=numpy.arange(n)
    y=scipy.tan(2*3.14*x)
    
    uiplot.pushButton_2.clicked.connect(lambda: timer.setInterval(5))
    uiplot.pushButton.clicked.connect(lambda: timer.setInterval(10000))
    uiplot.pushButton_3.clicked.connect(lambda: sms())
    
    
    
    c=Qwt.QwtPlotCurve()
    c.attach(uiplot.plot)
    
    timer = QtCore.QTimer()
    timer.start(5.0)
    win_plot.connect(timer, QtCore.SIGNAL('timeout()'),plot)
     
    win_plot.show()
    sys.exit(app.exec_())
    

