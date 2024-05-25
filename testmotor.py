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

print(sgn)
for i in range(len(sgn)):
    if int(sgn[i])==1:
        print(int(l0[i]))
        GPIO.output(int(l0[i]), GPIO.HIGH)

sleep(1)
GPIO.output(27,GPIO.LOW)
GPIO.output(22,GPIO.LOW)
GPIO.output(23,GPIO.LOW)
GPIO.output(24,GPIO.LOW)
GPIO.cleanup()

