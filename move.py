from camera import Cam
from line import Line

class Move:
    def __init__(self):
        self.__pc = Cam()
        self.__pc.camera_setup()
        
    def turn_left(self,t):
        pass
    def turn_right(self,t):
        pass
    def u_turn(self,t):
        pass
    def straight(self,t):
        pass

    def detect_green(self):
        src = self.__pc.take_picture()
        msk = self.__pc.process_image()
        res = self.__pc.get_img_direction(mask=msk)
        self.__pc.save_image(res[0])

class Detect:
    def __init__(self):
        self.mv = Move()
        self.ls = Line()

    def update(self):
        self.ls.update_sensor()

    def main(self):
        while True:
            self.update()

            if all(self.ls.sensors): #intersection [xxxxxxxx]

                if not self.mv.detect_green() or self.mv.detect_green[0]=="North": 
                    #S'il n'y a pas de vert avant l'intersection: cas simple
                    self.mv.straight(10) #avancer un peu puis re détecter car impossible
                                      #qu'il n'y ait pas de ligne droite ensuite

                elif self.mv.detect_green()==("South","Both"):
                    self.mv.u_turn()
                    self.mv.straight(10)
                    
                elif self.mv.detect_green()==("South","East"): #S'il ya du vert à droite avant l'intersection
                    self.mv.turn_right(100) #On tourne bien à droite
                    self.mv.straight(10)

                elif self.mv.detect_green()==("South","West"): #S'il y a du vert à gauche avant l'intersection
                    self.mv.turn_left(100) #On tourne bien à gauche
                    self.mv.straight(10)


            elif any(self.ls.center) and not any(self.ls.sides): #ligne noire droite au centre [___xx___]
                self.mv.straight(100)                         #le cas de base, on avance
                                                           #Même pas besoin de detect du vert



            elif not any(self.ls.sensors): #aucune ligne [________]
                pass                    #Le plus opti cest quoi?



            elif not any(self.ls.left) and all(self.ls.right): #ligne noire à droite [_____xxx]
                if self.mv.detect_green==("South","East"):  #Si ya du vert à droite
                    self.mv.turn_right(100)
                    self.mv.straight(10)
                else:
                    self.mv.straight(100) #Pas de vert = on IGNORE les intersections !!!



            elif not any(self.ls.right) and all(self.ls.left): #ligne noire à gauche [xxx_____]
                if self.mv.detect_green==("South","West"):  #Si ya du vert à gauche
                    self.mv.turn_left(100)
                    self.mv.straight(10)
                else:
                    self.mv.straight(100) #Pas de vert = on IGNORE les intersections !!!
        
        #<3

if __name__=="__main__":
    mv = Move()
    mv.detect_green()