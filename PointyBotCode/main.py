# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project Main File!

import RPi.GPIO as GPIO #import GPIO interface
import time, os, pygame, serial, sys
from pygame.locals import *   # for event MOUSE variables
import numpy as math
import GUIsetup as GUI
from getGPSData import * 
from GUIsetup import *
import moduleInfo, targetInfo, setTargets

#Set up Quit interrupt JUST IN CASE
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([27], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins as inputs
def GPIO27_callback(channel):
  print("Button 27 (Quit) has been pressed")
  GPIO.cleanup()
  os.system('pkill python')
  sys.exit()
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,bouncetime=300)

#Pygame GUI setup is handled while importing GUIsetup

#Get current position of the module (on startup)
getGPSData()

#Set initial target to immediately below the module (so that it points downwards after initializing)
# WHAT ARE THE VALUES FOR THIS
setTargets.pointDown()

#Buttons and other text to draw ont he screen (defs of {'Name':Location})
buttons, otherText = GUI.displayHome()

#Begin infinite loop of the program!
try:
 while True:
 
   #check for button presses, display position, and react according to which screen has been displayed
   for event in pygame.event.get():
     if(event.type is MOUSEBUTTONDOWN):
       pos = pygame.mouse.get_pos()
     elif(event.type is MOUSEBUTTONUP):
       pos = pygame.mouse.get_pos()
       x,y = pos
       #Flip the position if flipping the screen
       if GUI.runOnTFT:
         x = 320 - x
         y = 240 - y
 
       #Check through all the buttons currently being displayed on the screen & perform action based on what was clicked
       for button_text, button_location in buttons.items():
         text_surface = GUI.my_font.render(button_text, True, GUI.WHITE)
         button = text_surface.get_rect(center=button_location)
         button = button.inflate(30,30) #Inflates the hitboxes of buttons to make them easier to hit
         #Have button reactions occur if they have been pressed
         if button.collidepoint([x,y]):
           #print "Hit " + button_text + " button at " +str([x,y])
           #Main screen options: Pause/Resume, got to Settings, go to Targets, quit
           #if(button_text == 'Pause'):
           #  setTargets.stopPointing()
           #  buttons, otherText = GUI.displayHome()
           #elif (button_text == 'Resume'):
           #  setTargets.startPointing()
             #GUI.isTracking = not GUI.isTracking
             #GUIsetup.reload()
           #  buttons, otherText = GUI.displayHome()
           if(button_text == 'Settings'):
             buttons, otherText = GUI.displaySettings()
           elif(button_text == 'Targets'):
             buttons, otherText = GUI.displayTargets()
           #Settings screen options: update position, calibrate axes, calibrate orientation, return to home
           #Update position: runs code to update position in moduleInfo.py then returns to home screen
           elif(button_text == 'Update Position'):
             getGPSData()
             buttons, otherText = GUI.displayHome()
           #Calibrate orientation: says not currently functional then returns to home screen
 #          	if(button_text == "Get Orientation"):
 
           #Calibrate Axes: runs axes calibration [may cut this out if it dislikes being passed that info, since currently it requires deleting the config files and then restarting pointingProcess] then returns to home
           #Targets screen options: ISS, ECE 5725 Lab, Cuyler's House, Kristina's House, return to home
           #Track ISS: Sets targetInfo.py to ISS position, updating every 15 sec then returns home
           elif(button_text ==  'ISS Tracking'):
             setTargets.targetISS(True)
             buttons, otherText = GUI.displayHome()
           #Static targets: sets targetInfo.py to the static target and then returnb to home
           elif(button_text ==  'Point at Cuylers House'):
             setTargets.pointAtCuyler()
             buttons, otherText = GUI.displayHome()
           elif(button_text ==  'Point At Kristinas House'):
             setTargets.pointAtKristina()
             buttons, otherText = GUI.displayHome()
           elif(button_text ==  'Point At ECE5725 Lab'):
             setTargets.pointAtLab()
             buttons, otherText = GUI.displayHome()
           elif(button_text == 'Quit'):
             GPIO27_callback()
             buttons, otherText = GUI.displayHome()
           elif(button_text == 'Reboot'):
             os.system('sudo reboot -h now')
           elif(button_text == 'Power Off'):
             os.system('sudo shutdown -h now')
           elif(button_text ==  'Home'):
             buttons, otherText = GUI.displayHome()
 
 
   #%%%%%
   #Draw the new screen
   #%%%%%
   #Draw the buttons for this screen
   GUI.screen.fill(GUI.BLACK)
   for my_text, text_pos in buttons.items():
     text_surface = GUI.my_font.render(my_text, True, GUI.WHITE)
     rect = text_surface.get_rect(center=text_pos)
     GUI.screen.blit(text_surface,rect)
   #Draw Other text on the screen
   for my_text, text_pos in otherText.items():
     text_surface = GUI.my_font.render(my_text, True, GUI.WHITE)
     rect = text_surface.get_rect(center=text_pos)
     GUI.screen.blit(text_surface,rect)
   
   #Displays the new screen and limits FPS
   if GUI.runOnTFT:
     GUI.screen.blit(pygame.transform.rotate(GUI.screen, 180), (0, 0)) #Possible needed to flip screen
   pygame.display.flip()
   GUI.gameClock.tick(GUI.FPS)
   
except:
 GPIO.cleanup()
 exit()
