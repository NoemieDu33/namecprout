import RPi.GPIO as GPIO
import time

# définition des broches utilisées
broche_S3 = 27  # S0 du TSC3200 à GPIO27 du Raspberry Pi
broche_S2 = 22  # S1 du TSC3200 à GPIO22 du Raspberry Pi
broche_S1 = 23  # S2 du TSC3200 à GPIO23 du Raspberry Pi
broche_S0 = 24  # S3 du TSC3200 à GPIO24 du Raspberry Pi
broche_OUT = 17 # OUT du TSC3200 à GPIO25 du Rasperry Pi

GPIO.setmode(GPIO.BCM)
GPIO.setup(broche_OUT,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(broche_S0,GPIO.OUT)
GPIO.setup(broche_S1,GPIO.OUT)
GPIO.setup(broche_S2,GPIO.OUT)
GPIO.setup(broche_S3,GPIO.OUT)

# réglage de la fréquence de sortie du capteur (2% du maximum)
GPIO.output(broche_S0,GPIO.LOW)
GPIO.output(broche_S1,GPIO.HIGH)

def mesure():
    time.sleep(0.1)
    debut = time.time()
    for impulse_count in range(10):
        GPIO.wait_for_edge(broche_OUT, GPIO.FALLING)
    return time.time() - debut      

while(1):  

    GPIO.output(broche_S2,GPIO.LOW)
    GPIO.output(broche_S3,GPIO.LOW)
    rouge = mesure()
    print("Rouge: ",rouge)

    GPIO.output(broche_S2,GPIO.LOW)
    GPIO.output(broche_S3,GPIO.HIGH)
    bleu = mesure()
    print("Bleu: ",bleu)

    GPIO.output(broche_S2,GPIO.HIGH)
    GPIO.output(broche_S3,GPIO.HIGH)
    vert = mesure()
    print("Vert: ",vert)

    GPIO.output(broche_S2,GPIO.HIGH)
    GPIO.output(broche_S3,GPIO.LOW)
    total = mesure()
    print("Sans filtre: ",total)

  # ici, vous pouvez ajouter des conditions afin de détecter
  # un objet connu, par exemple:
  
    if ((abs(rouge - 0.22) < 0.02) and (abs(bleu - 0.25) < 0.02) and (abs(vert - 0.32) < 0.02)):
        print("C'est le carton noir!")

    print("\n")
    time.sleep(1)  