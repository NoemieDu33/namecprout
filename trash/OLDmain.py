
import time, math
import RPi.GPIO as gpio
from robot import MotorController
from line import line
# from accel import Accel # accelerometre
from green import DetectGreen # détection vert

#def de fréquence du PWM 
frequency = 1000
 # la valeur du pwm est comprise entre 0 et 100
duration = 0
gpio.setmode(gpio.BCM) # on l'appelle avant les instances de classe
# car les instances ont besoin du pinout set en BCM dans leur __init__
# et le mieux est d'appeler setmode une seule fois

gpio.setup(27, gpio.IN) # Pour le bouton

robot = MotorController()
lin = line()
# al = Accel()
dg = DetectGreen()
dg.start_cam()

button_pressed = False
# al.detect_pente -> 0 si terrain plat, -1 montée, 1 descente

def is_button_pressed()->bool:
    global button_pressed
    if gpio.input(27)==gpio.LOW: # si bouton en train d'être pressé...
        time.sleep(0.4) # On attend que l'user le relâche
        if gpio.input(27)==gpio.HIGH: # Si le bouton a été relâché, on compte ça comme un bouton pressé 
        # Par conséquent, si qqch tombe sur le bouton et appuie continuellement dessus, le robot ne s'arrêtera pas 
            button_pressed = not button_pressed # On inverse le booléen, le bouton a un rôle de switch entre True et False à chaque appui
    return button_pressed



while True : 
    if is_button_pressed():
        ret = None
        dg.take_picture()
        dg.process_image_green()
        res, r = dg.get_green_from_img_new()
        if r==False:
            ret = None
        else:
            ret = r
        
        if not lin.obstacle():
            robot.stop()
            print('stopobs')
            robot.evit_obstacle_par_droite()
            robot.ballayage_droite()

        elif ret is not None: #si on detecte du vert, le robot s'arrete et reprend le temps de detecter

            # if res[0] == res[1]: # demi tour
            #     robot.rotate(90,"right")
            #     time.sleep(1) # --------- 1 est beaucoup, non?
            #     etat = lin.sensor()
            #     while not any(etat):
            #         robot.rotate(90,"right")
            #         etat = lin.sensor()
            #     print("demi tour détecté")
    
            
            if res[1]>res[0]:
                robot.forward(70)
                time.sleep(0.3) # -------  c'est pas trop? Pourquoi l'avancer autant?
                robot.rotate(90, "right")
                time.sleep(0.6)
                etat = lin.sensor()
                while not any(etat):
                    robot.rotate(90,'right')
                    time.sleep(0.05)
                    robot.forward(70)
                    time.sleep(0.1)
                    etat = lin.sensor()
                print("droite détecté")


            
            elif res[0]>res[1]:
                robot.forward(70)
                time.sleep(0.35) # -------  Même remarque ici
                robot.rotate(70, "left")
                time.sleep(0.7)
                etat = lin.sensor()
                while not any(etat):
                    robot.rotate(90,'left')
                    etat = lin.sensor()
                print("gauche détecté")

        else:
            etat = lin.sensor()
            righ = etat[0] + etat[1] + etat[2] + etat[3]
            left  = etat[4] + etat[5] + etat[6] + etat[7]
            if etat[2]==1:
                if etat[0]==1 or etat[1]==1:
                    while( etat[0]== 1 or etat[1] == 1):
                        robot.rotate(80,'left')
                        etat = lin.sensor()

                        righ = etat[0]+ etat[1] + etat[2] + etat[3]
                        left  = etat[4] + etat[5] + etat[6] + etat[7] 
                    robot.rotate(90,'left')
                    time.sleep(0.03)
                    robot.stop()
                else: 
                    #robot.forwardENA(70)
                    #robot.forwardENB(100)
                    while(etat[3]== 0):
                        robot.rotate(80,'left')
                        etat = lin.sensor()
                        righ = etat[0] + etat[1] + etat[2] + etat[3]
                        left  = etat[4] + etat[5] + etat[6] + etat[7]
                    robot.forward(70)
                    time.sleep(0.015)
                    robot.stop()

            if etat[5]==1:
                if etat[7]==1 or etat[6]==1:
                    while( etat[7]== 1 or etat[6] == 1):
                        robot.rotate(80,'right')
                        etat = lin.sensor()
                        righ = etat[0]+ etat[1] + etat[2] + etat[3]
                        left  = etat[4] + etat[5] + etat[6] + etat[7] 
                    robot.rotate(90,'right')
                    time.sleep(0.03)
                    robot.stop()
                else: 
                    #robot.forwardENA(100)
                    #robot.forwardENB(70)
                    while(etat[4]==0):
                        robot.rotate(80,'right')
                        etat = lin.sensor()
                        righ = etat[0] + etat[1] + etat[2] + etat[3]
                        left  = etat[4] + etat[5] + etat[6] + etat[7]
                    robot.forward(70)
                    time.sleep(0.015)
                    robot.stop()

            elif(etat[3]== 1 or etat[4]==1) :      
                robot.forward(70)

            # elif(righ == 0  and left == 0): 
            #     robot.stop()
            #     time.sleep(0.05)
            #     while(righ == 0 and left == 0 and duration < 6000 ): 
            #         robot.forward(50)
            #         print('duration', duration )
            #         duration += 1 
            #         etat = lin.sensor()
            #         righ = etat[0] + etat[1] + etat[2] + etat[3]
            #         left  = etat[4] + etat[5] + etat[6] + etat[7]
            #     duration = 0 
            #     if(righ == 0 and left == 0 ): 
            #         while(righ == 0 and left == 0 ): 
            #             robot.backward(60)
            #             print('go backward, refine line')
            #             etat = lin.sensor()
            #             righ = etat[0] + etat[1] + etat[2] + etat[3]
            #             left  = etat[4] + etat[5] + etat[6] + etat[7]
            #         robot.stop()
            #         time.sleep(1)

            else:
                if(etat[7]== 1): 
                    robot.rotate(70,'right')

                elif(etat[0]== 1 ): 
                    robot.rotate(70,'left')
    else:
        robot.stop()




