from move import Move, Detect
from camera import Cam
# from accel import Accel
from line import Line
from motor import Motor

# Le contrôleur appelle tous les modèles!
# Si possible, éviter que les modèles s'appellent entre eux

cam = Cam()
lin = Line()
# acl = Accel()
mot = Motor()
mov = Move(cam, mot)
det = Detect(mov, lin) #classe principale