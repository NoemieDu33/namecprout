import RPi.GPIO as gpio
import time

class Motor:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.step_pin = 13 #13
        self.dir_pin = 17   #1

        gpio.setup(self.step_pin,gpio.OUT)
        self.pwm = gpio.PWM(self.step_pin, 0.5)
        gpio.setup(self.dir_pin,gpio.OUT)

    def one_full_turn(self):
        delay = 0.0005 #500microsecods
        gpio.output(self.dir_pin, gpio.HIGH)
        for x in range(200):
            self.pwm.start(100)
            #gpio.output(self.step_pin, gpio.HIGH)
            #print("High signal step")
            time.sleep(delay)
            self.pwm.stop()
            #gpio.output(self.step_pin, gpio.LOW)
            #print("Low signal step")
            time.sleep(delay)
        gpio.output([self.dir_pin, self.step_pin], gpio.LOW)
        


if __name__=="__main__":
    mot = Motor()
    mot.one_full_turn()
    gpio.cleanup()

