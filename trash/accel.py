# from mpu6050 import mpu6050
# sensor = mpu6050(0x53)
#for _ in range(200):
#    acc_data = sensor.get_accel_data()
#    print(acc_data)

from adxl345 import ADXL345
import time,os
  
class Accel:
    def __init__(self):
        self.pente = 0
        self.accel = ADXL345()
        self.axes = dict()
        
    def get_angles(self):
        self.axes = self.accel.getAxes(True)
#        os.system("clear")
#        print(f"""x={self.axes['x']}
#y={self.axes['y']}
#z={self.axes['z']}""")


    def detect_pente(self):
        self.get_angles()
        if self.axes['x']<=-0.2:
            if self.pente<5:
                print("Pente?")
                self.pente+=1
            else:
                print("Pente descendante")
                return 1
                
        elif self.axes['x']>=0.2:
            if self.pente>-5:
                print("Pente?")
                self.pente-=1
            else:
                print("Pente ascendante")
                return -1
                
        else:
            print("Terrain OK")
            if self.pente>0:
                self.pente-=1
            elif self.pente<0:
                self.pente+=1
            return 0



                
#    def detect_angle(self):
#        """Inutilisé"""
#        self.get_angles()
 #       pass
    

