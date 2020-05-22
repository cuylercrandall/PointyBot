# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project
#This file contains all the setup for our touchscreen GUI (to clean up the main.py file

import pygame, os, time
from pygame.locals import *   # for event MOUSE variables

#Variable to check if we're running on the TFT or not (to avoid repeated commenting)
runOnTFT = False
if runOnTFT:
  os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
  os.putenv('SDL_FBDEV', '/dev/fb1') #
  os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
  os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
  pygame.init()
  pygame.mouse.set_visible(False)
  #screen.blit(pg.transform.rotate(screen, 180), (0, 0)) #Possible needed to flip screen
else:
	pygame.init()

WHITE = 255, 255, 255
BLACK = 0,0,0
screen = pygame.display.set_mode((320, 240))
my_font= pygame.font.Font(None, 30)

gameClock = pygame.time.Clock()
FPS = 30

test = 1

#Variable for buttons to press (def of text and location)
buttons = {}

#Variable for other things to display
otherText = {}
circles = {}
isTracking = False

#Each function represents a different screen to display, each screen has both info and buttons
#"Home Screen" buttons/info
def displayHome():
  #Buttons on home screen: Targets, Settings, Pause/Resume
  if isTracking:
    buttons = {'Targets':(240,200),'Settings':(80,200),'Pause':(240,100)}
  else:
    buttons = {'Targets':(240,200),'Settings':(80,200),'Resume':(240,100)}
  #Other text on home screen: PointyBox!
  otherText = {'PointyBox!':(100,50)}
  
  return [buttons, otherText]
  
#"Setting screen" (options to calibrate different things)  
#def displaySettings():


#"Targets Screen" (options for different targets, currently ISS, ECE 5725 Lab, My House, Kristina's House)