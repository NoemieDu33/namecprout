import RPi.GPIO as gpio

class Line:
    def __init__(self):

        self.capt1, self.capt2 , self.capt3, self.capt4 = 5 , 6 , 7 , 8 #pins digital
        self.capt5, self.capt6,self.capt7, self.capt8 = 14 , 15 , 16 , 25 
        self.control = 26
        self.sensors = [0,0,0,0,0,0,0,0] # permet de stocker l'état des capteur 
        self.obstaclePIN = 1
        self.left = self.sensors[0:3]
        self.right = self.sensors[5:]
        self.center = self.sensors[3:5]
        self.sides = self.sensors[0:3] + self.sensors[5:]
        
        gpio.setmode(gpio.BCM)

        gpio.setup(self.capt1, gpio.IN)
        gpio.setup(self.capt2, gpio.IN)
        gpio.setup(self.capt3, gpio.IN)
        gpio.setup(self.capt4, gpio.IN)
        gpio.setup(self.capt5, gpio.IN)
        gpio.setup(self.capt6, gpio.IN)
        gpio.setup(self.capt7, gpio.IN)
        gpio.setup(self.capt8, gpio.IN)

        gpio.setup(self.control,gpio.OUT)
        gpio.setup(self.obstaclePIN,gpio.IN)

        gpio.output(self.control,gpio.HIGH)

    def obstacle(self): 
        obs = gpio.input(self.obstaclePIN)
        return obs

    def update_sensor(self): #sidestr "right" ou autre
        #gpio.output(self.control,gpio.LOW)
        self.sensors[0] = gpio.input(self.capt1)
        self.sensors[1] = gpio.input(self.capt2)
        self.sensors[2] = gpio.input(self.capt3)
        self.sensors[3] = gpio.input(self.capt4)
        self.sensors[4] = gpio.input(self.capt5)
        self.sensors[5] = gpio.input(self.capt6)
        self.sensors[6] = gpio.input(self.capt7)
        self.sensors[7] = gpio.input(self.capt8)

        self.left = self.sensors[0:3] # 0:4 pour [xxxx____], 0:3 pour [xxx_____]
        self.right = self.sensors[5:] # 4: pour [____xxxx], 5: pour [_____xxx]
        self.center = self.sensors[3:5] # 2:6 pour [__xxxx__], 3:5 pour [___xx___]
        self.sides = self.sensors[0:3] + self.sensors[5:] # [xxx__xxx]

    #print("État de la sortie :", self.capt)
        return self.sensors
        #gpio.output(self.control,gpio.HIGH)

