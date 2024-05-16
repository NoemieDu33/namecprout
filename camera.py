import numpy as np
import cv2 as cv
from picamera2 import MappedArray, Picamera2, Preview
import math
import sys, random

class Cam:
    def __init__(self):
        self.picam = Picamera2()
            
    def camera_setup(self, length=1532, height=864):
        modes = self.picam.sensor_modes
        mode = modes[0]
        config = self.picam.create_preview_configuration(sensor={'output_size': mode['size']})
        self.picam.configure(config)
        self.picam.start_preview(Preview.NULL)
        self.picam.start()

    def take_picture(self):
        array = self.picam.capture_array()
        # array = cv.resize(array, (0,0), fx=0.5, fy=0.5) 
        return array

    def save_image(self, src):
        cv.imwrite(f"output{random.randint(1, random.randint(1,10000000))}.png",src)

    #-----------------------------------

    @staticmethod  
    def process_image(src):
        hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)

        lower_green = np.array([40, 20, 50])
        upper_green = np.array([90, 255, 255])

        # create a mask for green color
        mask_green = cv.inRange(hsv, lower_green, upper_green)
        return mask_green

    @staticmethod
    def get_img_direction(src, mask)->list:

        list_green_squares = []

        contours_green, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # loop through the green contours and draw a rectangle around them
        for cnt in contours_green:
            contour_area = cv.contourArea(cnt)
            if contour_area > 2000: # Si faux positif: augmenter, si faux nÃ©gatif: rÃ©duire. Default: 1000
                x, y, w, h = cv.boundingRect(cnt)

                directions = {
                    "South" : 0,
                    "North" : 0,
                    "West" : 0,
                    "East" : 0
                }

                # Pixel à droite du bord droite : src[y+(h//2), x+w+i_]
                # à gauche du bord gauche : src[y+(h//2), x-i_]
                # au dessus du bord supérieur : src[y-i_, x+(w//2)]
                # en dessous du bord inférieur : src[y+h+i_, x+(w//2)]

                for i_ in range(1,6):
                    try:
                        pxl_east = src[y+(h//2), x+w+i_]
                        pxl_west = src[y+(h//2), x-i_]
                        pxl_north = src[y-i_, x+(w//2)]
                        pxl_south = src[y+h+i_, x+(w//2)]
                    except Exception as exc: 
                        continue

                    if sum(pxl_east)-255 < 240 : # Si ligne noire à l'Est alors vert à l'Ouest
                        directions["West"]+=1
                    if sum(pxl_west)-255 < 240 :
                        directions["East"]+=1
                    if sum(pxl_north)-255 < 240 : # Même logique, si ligne noire au nord alors carré au Sud 
                        directions["South"] += 1
                    if sum(pxl_south)-255 < 240 : 
                        directions["North"] += 1

                list_green_squares.append(directions)




                cv.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
        list_final_directions = []

        for elt in list_green_squares:
            if elt["South"]>elt["North"]:
                if elt["East"]>elt["West"]:
                    list_final_directions.append("S-E")
                else:
                    list_final_directions.append("S-W")
                # else:
                #     if elt["East"]>elt["West"]:
                #         list_final_directions.append("N-E")
                #     else:
                #         list_final_directions.append("N-W")

        if not len(list_final_directions):
            print("Rien?!")
        if len(list_final_directions)==1:
            print(list_final_directions[0])
            if list_final_directions[0]=="S-W":
                print("GAUCHE !")
            else:
                print("DROITE !")
        else:
            if "S-E" and "S-W" in list_final_directions:
                print("S-Both")
                print("DEMI TOUR !")
        

        
                # cv.circle(src, center_of_rectangle, 4, (255, 0, 0), 4)
                # cv.line(src, (src.shape[1]//2, src.shape[0]), center_of_rectangle,(0,0,255),2)
        return (src, list_final_directions)




# #test_img = cv.imread("20240302_124156.jpg")
# #testresized = test_img #= cv.resize(test_img, (0,0), fx = 0.2, fy = 0.2)
# def process_image_circle(src):
#     #redimensionne l'img, on pourra le retirer quand on rÃ©glera la rÃ©solution de la picamera
#     src = cv.resize(src, (0,0), fx = 1.5, fy = 1.5)
#     #HoughCircles doit recevoir en paramÃ¨tre une img noire et blanche donc conversion   
#     gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
#     gray = cv.medianBlur(gray, 5)
#     return gray # On retourne l'image prÃªte Ã  Ãªtre analysÃ©e

# def get_circle_from_img(src):
#     # les shape d'array numpy renvoient le tuple (hauteur, longueur, dimensions)
#     rows = src.shape[0]
#     columns = src.shape[1]
#     circles = cv.HoughCircles(src, cv.HOUGH_GRADIENT, 1, rows / 8,
#                             param1=100, param2=30,
#                             minRadius=0, maxRadius=0) 
#     #Beaucoup de paramÃ¨tres influant la dÃ©tection des cercles, mais pas besoin de les changer
#     # Les valeurs Ã©gales Ã  0 permettent de dire qu'on connait pas les propriÃ©tÃ©s des cercles qu'on
#     # veut analyser, donc go pas les modifier


#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         #for i in circles[0, :]:
#         i = circles[0,:][0] # S'il y a plusieurs balles Ã§a dÃ©tectera que la 1re
#         center = (i[0], i[1])
#         # circle center
        
#         # circle outline
#         radius = i[2]
#         direction = 1 # 1 = droite, 0 = tout droit, -1 = gauche. Par dÃ©faut, droite
        

#         adjacentLongueurPx = rows-center[1]
#         opposeLongueurPx = center[0]-columns//2
#         angle = math.degrees(math.atan(opposeLongueurPx / adjacentLongueurPx))

#         if angle<0: #angle < 0 --> Faut tourner Ã  gauche
#             direction = -1
#             angle = abs(angle)
#         angleround = round(angle, 2)
#         if angleround < 3:
#             angleround, direction = 0,0 # S'il faut tourner moins que 3Â°, on annule l'angle

#         # LÃ  c'est les dessins sur l'image
#         cv.circle(src, center, 1, (0, 100, 100), 3) # Le centre
#         cv.circle(src, center, radius, (0, 0, 255), 3) # Le contour du cercle
#         cv.line(src,(columns//2,rows),(columns//2,center[1]),(0,255,0),2) # Ligne droite depuis l'oeil du robot
#         cv.line(src, (columns//2, rows),center,(255,0,0),3) # La ligne du robot vers le centre du cercle
#         cv.line(src, (columns//2, center[1]),center,(0,165,255),2) # Ligne horizontale pour complÃ©ter le triangle
        
#         #Texte sur l'image
#         cv.putText(src, f"Angle de rotation = {str(angleround)} deg a {'gauche' if direction<0 else 'droite'}", (50,50), cv.FONT_HERSHEY_SIMPLEX ,  
#                 1, (255,0,0), 2, cv.LINE_AA)
#     else:
#         return -1 #Pas de balle dÃ©tectÃ©e
#     return src
