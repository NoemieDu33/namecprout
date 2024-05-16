from camera import Cam
import time

class Move:
    def __init__(self):
        self.__pc = Cam()
        self.__pc.camera_setup()
        self.final = []
        
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
        self.final, res = self.__pc.get_img_direction(src=src, mask=msk)

    def end_this(self):
        self.__pc.save_image(src=self.final)
    

if __name__=="__main__":
    mv = Move()
    for _ in range(30):
        mv.detect_green()
        time.sleep(0.2)
    mv.end_this()