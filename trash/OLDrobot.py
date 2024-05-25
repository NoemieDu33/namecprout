import math, time
import RPi.GPIO as gpio
from line import line

class MotorController:
    def __init__(self):

        self.IN1, self.IN2, self.IN3, self.IN4 = 17, 22, 23, 24 #pins digital
        self.EnA, self.EnB = 12,13 #pwm0 et pwm1

        # speed = fréquences en Hz
        self.right_speed = 0 #EnB
        self.left_speed = 0 # EnA
        frequency = 1000    # setup la fréquence des pin PWM

        self.line_model = line()
        

        gpio.setup(self.IN1, gpio.OUT)
        gpio.setup(self.IN2, gpio.OUT)
        gpio.setup(self.IN3, gpio.OUT)
        gpio.setup(self.IN4, gpio.OUT)
        gpio.setup(self.EnA, gpio.OUT)
        gpio.setup(self.EnB, gpio.OUT)
        
        

        self.pENA = gpio.PWM(self.EnA, frequency)
        self.pENB = gpio.PWM(self.EnB, frequency)
        
        self.pENA.start(50)
        self.pENB.start(50)

        self.stop()
        
#to do ==> faire en sorte que si le nombre que l'on aplique a la fonctiodn est supérieur à 100 alors on retourne une rreur 
        


    def set_speed(self, sidestr, value): #sidestr "right" ou autre
        side = -1
        if sidestr.strip().lower()=="right":
            side = 1
        elif sidestr.strip().lower()=="left":
            side=0
        if side == -1:
            raise ValueError(f"\"right\" or \"left\" expected, got \"{sidestr}\"")
        
        if side: 
            self.right_speed = value
        else:
            self.left_speed = value
    
   ## cotrol du moteur ENA indépendament
             
    def forwardENA(self,speed): 
        self.pENA.ChangeDutyCycle(speed)
        gpio.output(self.IN1, gpio.LOW)
        gpio.output(self.IN2, gpio.HIGH)
    
    def backwardENA(self,speed): 
        self.pENA.ChangeDutyCycle(speed)
        gpio.output(self.IN1,gpio.HIGH)
        gpio.output(self.IN2,gpio.LOW)
    
    def stopENA(self): 
        self.pENA.ChangeDutyCycle(0)
        gpio.output(self.IN1,gpio.LOW)
        gpio.output(self.IN2,gpio.LOW)

# control du mtoeur ENA indépendament
    def stop(self): 
        self.stopENA()
        self.stopENB()
    def forwardENB(self,speed): 
        self.pENB.ChangeDutyCycle(speed)
        gpio.output(self.IN3, gpio.LOW)
        gpio.output(self.IN4, gpio.HIGH)
    
    def backwardENB(self,speed): 
        self.pENB.ChangeDutyCycle(speed)
        gpio.output(self.IN3,gpio.HIGH)
        gpio.output(self.IN4,gpio.LOW)
    
    def stopENB(self): 
        self.pENB.ChangeDutyCycle(0)
        gpio.output(self.IN3,gpio.LOW)
        gpio.output(self.IN4,gpio.LOW)


    def forward(self, speed):
        gpio.output(self.IN1, gpio.LOW)
        gpio.output(self.IN2, gpio.HIGH)
        gpio.output(self.IN3, gpio.LOW)
        gpio.output(self.IN4, gpio.HIGH)
        self.pENA.ChangeDutyCycle(speed) 
        self.pENB.ChangeDutyCycle(speed)
    

    def backward(self, speed):    
        gpio.output(self.IN1, gpio.HIGH)
        gpio.output(self.IN2, gpio.LOW)
        gpio.output(self.IN3, gpio.HIGH)
        gpio.output(self.IN4, gpio.LOW)
        self.pENA.ChangeDutyCycle(speed) 
        self.pENB.ChangeDutyCycle(speed)

    def rotate(self, speed, sens):
        self.pENA.ChangeDutyCycle(speed) 
        self.pENB.ChangeDutyCycle(speed)

        clockwise = -1
        if sens.strip().lower()=="right":
            clockwise = 0
        elif sens.strip().lower()=="left":
            clockwise=1
        if clockwise == -1:
            raise ValueError(f"\"right\" or \"left\" expected, got \"{sens}\"")

        if clockwise:
            gpio.output(self.IN1, gpio.HIGH)
            gpio.output(self.IN2, gpio.LOW)
            gpio.output(self.IN3, gpio.LOW)
            gpio.output(self.IN4, gpio.HIGH)
        else:
            gpio.output(self.IN1, gpio.LOW)
            gpio.output(self.IN2, gpio.HIGH)
            gpio.output(self.IN3, gpio.HIGH)
            gpio.output(self.IN4, gpio.LOW)
        
    # test des moteur 
#######
#######
    def sequential_motor(self,speed):  
        self.forwardENA(speed)
        time.sleep(1)
        self.stopENA()
        time.sleep(1)
        self.backwardENA(speed)
        time.sleep(1)
        self.stopENA()
        time.sleep(1)
        self.forwardENB(speed)
        time.sleep(1)
        self.stopENB()
        time.sleep(1)
        self.backwardENB(speed)
        time.sleep(1)
        self.stopENB()
        time.sleep(1)


    
    def evit_obstacle_par_droite(self): 
    
        self.backward(60)
        time.sleep(0.5)
        self.rotate(95,'right')
        time.sleep(0.2)
        self.forward(60)
        time.sleep(1.5)
        self.rotate(95,'left')
        time.sleep(0.6)
        self.forward(65)
        time.sleep(1.4)
        self.rotate(90,'right')
        time.sleep(0.32)
        self.backward(60)
        time.sleep(0.8)
        self.stop()

    def ballayage_droite(self): 

        etat_line =self.line_model.sensor()
        turn = 0
        while( not any(etat_line) and turn <= 3000): 
            turn += 1 
            etat_line =self.line_model.sensor()
            self.rotate(70,'left')
        turn = 0
        while( not any(etat_line) and turn <=  7000): 
            turn += 1 
            etat_line =self.line_model.sensor()
            self.rotate(70,'right')
        self.stop()



    def evit_obstacle_par_gauche(self):

        self.backward(60)
        time.sleep(0.5)
        self.rotate(95,'left')
        time.sleep(0.2)
        self.forward(50)
        time.sleep(2)
        self.rotate(95,'right')
        time.sleep(0.5)
        self.forward(50)
        time.sleep(1.7)
        self.rotate(90,'left')
        time.sleep(0.35)
        self.backward(50)
        time.sleep(0.6)
        self.stop()  


      