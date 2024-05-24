import RPi.GPIO as gpio
import time

class Motor:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self.step_pin = 13 #13
        self.dir_pin = 17   #1

        gpio.setup(self.step_pin,gpio.OUT)
        gpio.setup(self.dir_pin,gpio.OUT)

    def one_full_turn(self):
        delay = 0.0005 #500
        gpio.output(self.dir_pin, gpio.HIGH)
        for x in range(200):
            gpio.output(self.step_pin, gpio.HIGH)
            print("High signal step")
            time.sleep(delay)
            gpio.output(self.step_pin, gpio.LOW)
            print("Low signal step")
            time.sleep(delay)


if __name__=="__main__":
    mot = Motor()
    mot.one_full_turn()
    gpio.cleanup()

