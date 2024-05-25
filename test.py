from line import Line
import time

li = Line()
for _ in range(100):
    li.update_sensor()
    print(li.sensors)