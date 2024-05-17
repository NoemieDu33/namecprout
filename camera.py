import numpy as np
import cv2 as cv
imps = True
try:
    from picamera2 import MappedArray, Picamera2, Preview
    from libcamera import Transform
except Exception:
    imps = False
    print("(imports) WARNING: picamera2 / libcamera librairies were not loaded.\nCamera mode will be disabled.")
import math
import sys, random
from datetime import datetime

class Cam:
    def __init__(self):
        self.img = sys.argv[1]
        if isinstance(self.img, str) and self.img!="take":
            self.img = cv.imread(f"{sys.argv[1]}")

            
        if imps:
            self.picam = Picamera2()
        self.img_f = None
        self.img_c = None
            
    def camera_setup(self):
        if not imps:
            print("(camera_setup) WARNING: Camera modules aren't loaded!")
            return False
        # modes = self.picam.sensor_modes
        # mode = modes[0]
        # config = self.picam.create_preview_configuration(sensor={'output_size': mode['size']})
        # self.picam.configure(config)
        cfg = self.picam.create_still_configuration(transform=Transform(hflip=1, vflip=1))
        self.picam.configure(cfg)
        # self.picam.hflip = True
        # self.picam.vflip = True
        # self.picam.start_preview(Preview.NULL)
        self.picam.start()

    def take_picture(self):
        if imps and self.img=="take":
            try:
                array = self.picam.capture_array()
                array = cv.resize(array, (0,0), fx=0.2, fy=0.2)
                self.img_c = np.copy(array)
                self.img_f = cv.cvtColor(array, cv.COLOR_RGB2GRAY) 
                return array
            except Exception:
                print("FATAL: Picture couldn't be taken.\nIs the camera set up propely?\nDid you do camera_setup()?")
                exit()
        elif not imps and not isinstance(self.img, str):
            try:
                self.img_c = np.copy(self.img)
                self.img_f =cv.cvtColor(self.img, cv.COLOR_RGB2GRAY)
                return self.img
            except Exception:
                print(f"FATAL: Could not load image \"{sys.argv[1]}\".\nDid you forget the extension?\nDid you mistype the name?")
                exit()
        else:
            print("FATAL: Program started as take picture mode\nBut couldn't load camera modules.\nDoes it run on Raspberry?")
            exit()

    def save_image(self, src):
        cv.imwrite(f"output_{datetime.now()}.png",src)

    #-----------------------------------

    def process_image(self):
        hsv = cv.cvtColor(self.img_c, cv.COLOR_BGR2HSV)

        lower_green = np.array([25, 40, 25])
        upper_green = np.array([90, 255, 255])

        # create a mask for green color
        mask_green = cv.inRange(hsv, lower_green, upper_green)
        return mask_green

    def get_img_direction(self, mask)->list:

        list_green_squares = []

        contours_green, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # loop through the green contours and draw a rectangle around them
        for cnt in contours_green:
            contour_area = cv.contourArea(cnt)
            if contour_area > 2000: # Si faux positif: augmenter, si faux nÃ©gatif: rÃ©duire. Default: 1000
                x, y, w, h = cv.boundingRect(cnt)

                im_bw = cv.threshold(self.img_f, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                res = cv.bitwise_or(im_bw, mask)
                res = cv.cvtColor(res, cv.COLOR_GRAY2RGB)

                directions = {
                    "South" : 0,
                    "North" : 0,
                    "West" : 0,
                    "East" : 0
                }

                th = 50 # Baisser si mauvais placement des cardinaux du carré (plusieurs cardinaux opposés >0)
                        # Augmenter si aucun cardinal (plusieurs cardinaux opposés==0)
                # N'A UN EFFET QUE SI L'IMAGE ANALYSEE N'EST PAS BINARISEE.

                for i_ in range(1,10):
                    try:
                        pxl_east = res[y+(h//2), x+w+i_]
                    except Exception as exc: 
                        pxl_east = (255,255,255,255)
                    try:
                        pxl_west = res[y+(h//2), x-i_]
                    except Exception as exc: 
                        pxl_west = (255,255,255,255)
                    try:
                        pxl_north = res[y-i_, x+(w//2)]
                    except Exception as exc: 
                        pxl_north = (255,255,255,255)
                    try:
                        pxl_south = res[y+h+i_, x+(w//2)]
                    except Exception as exc: 
                        pxl_south = (255,255,255,255)

                    if sum(pxl_east)-255 < th : # Si ligne noire à l'Est alors vert à l'Ouest
                        directions["West"]+=1
                    if sum(pxl_west)-255 < th :
                        directions["East"]+=1
                    if sum(pxl_north)-255 < th : # Même logique, si ligne noire au nord alors carré au Sud 
                        directions["South"] += 1
                    if sum(pxl_south)-255 < th : 
                        directions["North"] += 1

                list_green_squares.append(directions)
                cv.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), -1)
                
                
        list_final_directions = []
        #print(f"{list_green_squares=}", "\n-")
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
            else:
                if elt["East"]>elt["West"]:
                    list_final_directions.append("N-E")
                else:
                    list_final_directions.append("N-W")
        if not len(list_final_directions):
            print("(Detect) : No green tile.")
        while "N-W" in list_final_directions:
            list_final_directions.remove("N-W")
            print("(Detect) : N-W green tile detected and removed.")
        while "N-E" in list_final_directions:
            list_final_directions.remove("N-E")
            print("(Detect) : N-E green time detected and removed.")
        if len(list_final_directions)==1:
            
            if list_final_directions[0]=="S-W":
                print("(Detect) : Turn left.")
            else:
                print("(Detect) : Turn right.")
        else:
            if "S-E" and "S-W" in list_final_directions:
                print("(Detect) : U-Turn.")
        

        
                # cv.circle(src, center_of_rectangle, 4, (255, 0, 0), 4)
                # cv.line(src, (src.shape[1]//2, src.shape[0]), center_of_rectangle,(0,0,255),2)
        #print(f"{list_final_directions=}")
        return (res, list_final_directions)


if __name__=="__main__":
    c = Cam()
    c.camera_setup()
    c.take_picture()
    msk = c.process_image()
    res = c.get_img_direction(mask=msk)
    c.save_image(res[0])













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
