from move import Move
from motor import Motor
import time

mot = Motor()
mov = Move(None, mot)

mov.straight(3)
mov.end()