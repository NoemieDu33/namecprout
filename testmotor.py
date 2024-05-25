import sys
from time import sleep        
import RPi.GPIO as GPIO        

sgn = str(sys.argv[1])

GPIO.setmode(GPIO.BCM)

GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

l0 = [27,22,23,24]
l1 = []


for i in range(len(sgn)):
    if int(sgn[i])==1:
        l1.append(l0[i])

GPIO.output([l1], GPIO.HIGH)
sleep(1)
GPIO.output([l0],GPIO.LOW)
GPIO.cleanup()

