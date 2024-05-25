from camera import Cam
from line import Line
from motor import Motor
import time

class Move:
    def __init__(self, pc:Cam, mt:Motor):
        self.__pc = pc
        if self.__pc!=None:
            self.__pc.camera_setup()
        self.__mt = mt
        
    def turn_left(self,t):
        self.__mt.send_signal(t, "left")
        
    def turn_right(self,t):
        self.__mt.send_signal(t, "right")

    def u_turn(self,t):
        self.__mt.send_signal(t, "U")

    def straight(self,t):
        self.__mt.send_signal(t, "forward")

    def back(self,t):
        self.__mt.send_signal(t, "back")
    
    def stop(self, t):
        self.__mt.send_signal(t,"stop")
    
    def avoid_right(self):
        self.__mt.send_signal(0.3, "back")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "right")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "forward")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "left")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "forward")
        time.sleep(0.2)
        self.__mt.send_signal(0.1, "right")
        time.sleep(0.2)
        self.__mt.send_signal(1, "stop")

    def avoid_left(self):
        self.__mt.send_signal(0.3, "back")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "left")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "forward")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "right")
        time.sleep(0.2)
        self.__mt.send_signal(0.2, "forward")
        time.sleep(0.2)
        self.__mt.send_signal(0.1, "left")
        time.sleep(0.2)
        self.__mt.send_signal(1, "stop")

    def end(self):
        self.__mt.terminate()

    # def detect_green(self):
    #     if self.__pc!=None:
    #         src = self.__pc.take_picture()
    #         msk = self.__pc.process_image()
    #         res = self.__pc.get_img_direction(mask=msk)
    #         self.__pc.save_image(res[0])

class Detect:
    def __init__(self, mv:Move, ls:Line):
        self.mv = mv
        self.ls = ls

    def update(self):
        self.ls.update_sensor()

    def main(self):
        while True:
            self.update()

            if any(self.ls.left):
                if sum(self.ls.left)>=2:
                    while sum(self.ls.left)>=2:
                        self.mv.turn_left(0.2)
                        self.ls.update_sensor()
                    self.mv.stop()

                else:
                    while not any(self.ls.center):
                        self.mv.turn_left(0.2)
                        self.ls.update_sensor()
                    self.mv.straight(0.1)
                    self.mv.stop()
            
            if any(self.ls.right):
                if sum(self.ls.right)>=2:
                    while sum(self.ls.right)>=2:
                        self.mv.turn_right(0.2)
                        self.ls.update_sensor()
                    self.mv.stop()

                else:
                    while not any(self.ls.center):
                        self.mv.turn_right(0.2)
                        self.ls.update_sensor()
                    self.mv.straight(0.1)
                    self.mv.stop()
            
            if any(self.ls.center):
                self.mv.straight(0.2)

            else:
                if self.ls.sensors[-1]:
                    self.mv.turn_right(0.1)
                elif self.ls.sensors[0]:
                    self.mv.turn_left(0.1)

        #<3

if __name__=="__main__":
    mv = Move()
    mv.detect_green()