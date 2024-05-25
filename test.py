from motor import Motor
import time,sys
import RPi.GPIO as gpio  

mo = Motor()
 
gpio.setmode(gpio.BCM)
gpio.setup(27, gpio.OUT) # avant gauche
gpio.setup(22, gpio.OUT) # arriere gauche
gpio.setup(23, gpio.OUT) # avant droit
gpio.setup(24, gpio.OUT) # arriere droit    
gpio.output(22, gpio.HIGH)
gpio.output(24, gpio.HIGH)