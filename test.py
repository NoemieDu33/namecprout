from move import Move
from motor import Motor
import time

mot = Motor()
mov = Move(None, mot)

print("straight")
mov.straight(2)
print("stop")
mov.stop(2)
mov.end()