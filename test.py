from move import Move
from motor import Motor
import time

mot = Motor()
mov = Move(None, mot)

mov.straight(2)
mov.stop(2)
mov.end()