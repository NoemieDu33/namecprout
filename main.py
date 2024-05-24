from move import Move, Detect
from camera import Cam
from accel import Accel
from line import Line
from motor import Motor

# Le contrôleur appelle tous les modèles!
# Si possible, éviter que les modèles s'appellent entre eux

cam = Cam()
mov = Move(cam)
lin = Line()
det = Detect(mov, lin) #classe principale
acl = Accel()
mot = Motor()