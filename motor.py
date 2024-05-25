import sys
import time       
import RPi.GPIO as gpio  

class Motor:
    def __init__(self):
        """
        0000 stop

        0010 virage à gauche
        1000 virage à droite

        1010 avancer
        0101 reculer

        1001 / 0110 demi-tour
        """
        gpio.setmode(gpio.BCM)
        gpio.setup(27, gpio.OUT) # avant gauche
        gpio.setup(22, gpio.OUT) # arriere gauche
        gpio.setup(23, gpio.OUT) # avant droit
        gpio.setup(24, gpio.OUT) # arriere droit    


    def send_signal(t, args):
        for i in range(len(args)):
            if i==0 and int(args[i])==1:
                gpio.output(27,gpio.HIGH)   
            if i==1 and int(args[i])==1:
                gpio.output(22,gpio.HIGH)   
            if i==2 and int(args[i])==1:
                gpio.output(23,gpio.HIGH)   
            if i==3 and int(args[i])==1:
                gpio.output(24,gpio.HIGH)  

        time.sleep(t)

        gpio.output(27,gpio.LOW)
        gpio.output(22,gpio.LOW)
        gpio.output(23,gpio.LOW)
        gpio.output(24,gpio.LOW)

    def terminate(self):
        gpio.cleanup()
        exit()

