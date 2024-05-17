import numpy as np
import cv2 as cv
import math
import sys, random
from datetime import datetime

class Cam:
    def __init__(self,img):
        self.img = cv.imread(img)
        self.img_c = cv.cvtColor(self.img, cv.COLOR_RGB2GRAY)
        self.img_f = np.copy(self.img)
        self.xy = []

    def save_image(self, x):
        cv.imwrite(f"erzgERZHGYZR.png",x[0])
    #-----------------------------------

    def process_image(self):
        hsv = cv.cvtColor(self.img, cv.COLOR_BGR2HSV)

        lower_green = np.array([25, 120, 25])
        upper_green = np.array([90, 255, 255])

        # create a mask for green color
        mask_green = cv.inRange(hsv, lower_green, upper_green)
        return mask_green

    def get_img_direction(self, mask)->list:
        print("-----\nBEGIN PRINT")

        list_green_squares = []

        contours_green, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        # loop through the green contours and draw a rectangle around them
        for cnt in contours_green:
            contour_area = cv.contourArea(cnt)
            if contour_area > 2000: # Si faux positif: augmenter, si faux nÃ©gatif: rÃ©duire. Default: 1000
                x, y, w, h = cv.boundingRect(cnt)

                im_bw = cv.threshold(self.img_c, 128, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]
                res = cv.bitwise_or(im_bw, mask)
                res = cv.cvtColor(res, cv.COLOR_GRAY2RGB)

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

                th = 50 # Baisser si mauvais placement des cardinaux du carré (plusieurs cardinaux opposés >0)
                        # Augmenter si aucun cardinal (plusieurs cardinaux opposés==0)

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
        print(f"{list_green_squares=}", "\n-")
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
        print(list_final_directions)
        if not len(list_final_directions):
            print("Rien?!")
        while "N-W" in list_final_directions:
            list_final_directions.remove("N-W")
        while "N-E" in list_final_directions:
            list_final_directions.remove("N-E")
        if len(list_final_directions)==1:
            
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
        print(f"{list_final_directions=}")
        print("END PRINT")
        return (res, list_final_directions)



if __name__=="__main__":
    c = Cam("ot.png")
    msk = c.process_image()
    res = c.get_img_direction(mask=msk)
    c.save_image(res)
    