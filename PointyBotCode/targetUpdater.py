# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Projec

import RPi.GPIO as GPIO
import os, time
from setTargets import *

#Adds physical escape button on TFT button
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([22, 27, 23, 17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins as inputs with pull up
#Defining callbacks for PiTFT buttons
def GPIO27_callback(channel):
  print("Button 27 (Quit) has been pressed")
  GPIO.cleanup()
  exit()
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,bouncetime=300)
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO27_callback,bouncetime=300)

lastUpdate = time.time()-15

while True:
  if time.time() - lastUpdate > 15:
    targetISS()
    lastUpdate = time.time()
  else:
    time.sleep(1)
