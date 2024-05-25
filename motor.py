import sys
import time       
import RPi.GPIO as gpio  

class Motor:
    def __init__(self):

        gpio.setmode(gpio.BCM)
        gpio.setup(27, gpio.OUT) # avant gauche
        gpio.setup(22, gpio.OUT) # arriere gauche
        gpio.setup(23, gpio.OUT) # avant droit
        gpio.setup(24, gpio.OUT) # arriere droit    


    def send_signal(self, args):
        if_sleep = False
        if args!="stop":
            if_sleep=True
            if args=="forward":
                gpio.output(27, gpio.HIGH)
                
            elif args=="right":
                gpio.output(27, gpio.LOW)
            elif args=="left":
                gpio.output(23, gpio.HIGH)
            elif args=="back":
                gpio.output(22, gpio.HIGH)
                gpio.output(24, gpio.HIGH)
            elif args=="U":
                gpio.output(22, gpio.HIGH)
                gpio.output(23, gpio.HIGH)

        

    def terminate(self):
        gpio.cleanup()
        exit()

