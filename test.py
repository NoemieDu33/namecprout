from camera import Cam
import time

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
        msk = self.__pc.process_image(src)
        res = self.__pc.get_img_direction(src=src, msk=msk)[1]
    

if __name__=="__main__":
    mv = Move()
    for _ in range(100):
        mv.detect_green()
        time.sleep(0.2)