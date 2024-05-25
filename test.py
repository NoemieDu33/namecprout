from line import Line
import time, RPi.GPIO

li = Line()
for _ in range(100):
    li.update_sensor()
    print(li.sensors)
    time.sleep(0.5)
RPi.GPIO.cleanup()