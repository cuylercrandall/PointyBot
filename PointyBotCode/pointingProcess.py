# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project 

import RPi.GPIO as GPIO
import os, time, sys
import numpy as math
import moduleInfo, targetInfo
from ourEncoders import *
from ourServos import *
from ourAxes import *
import outputWiringConfig as config
import pymap3d

#Adds physical escape button on TFT button
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([22, 27, 23, 17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins as inputs with pull up
#Defining callbacks for PiTFT buttons
def GPIO17_callback(channel):
  print("Button 17 (Quit) has been pressed")
  GPIO.cleanup()
  os.system('pkill python')
  #os.system('pkill -f main')
  sys.exit()
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)

#Setup of the axes to position
GPIO.setup([config.rotationServoPin,config.elevationServoPin], GPIO.OUT)
rotationAxis = axis(config.rotationServoPin,config.rotationEncoderChannel,"Rotation")
elevationAxis = axis(config.elevationServoPin,config.elevationEncoderChannel,"Elevation")

#Initializing other useful variables
targetTimestamp = os.stat("/home/pi/PointyBot/PointyBotCode/targetInfo.py")[8]
moduleTimestamp = os.stat("/home/pi/PointyBot/PointyBotCode/moduleInfo.py")[8]
targetUpdateTime = time.time()-70 #-60 triggers the update loop on first iteration
lastMoved = time.time()

try:
 #Outer while loop: infinitely looping
 while True:
   
   #Check if the info files have been changed (or every 60 seconds)
   targetTimestampTemp = os.stat("/home/pi/PointyBot/PointyBotCode/targetInfo.py")[8]
   moduleTimestampTemp = os.stat("/home/pi/PointyBot/PointyBotCode/moduleInfo.py")[8]
   if ((not moduleTimestamp==moduleTimestampTemp) or (not targetTimestamp==targetTimestampTemp)) or (time.time() - targetUpdateTime > 60):
     
     #If either has, set the new timestamp as the baseline (for both) then recalculate pointing
     targetTimestamp = targetTimestampTemp
     moduleTimestamp = moduleTimestampTemp
     targetUpdateTime = time.time()
     lastMoved = time.time()
     moduleInfo = reload(moduleInfo)
     targetInfo = reload(targetInfo)
     
     #Generates enu-centric pointing vector
     vector_enu = math.array(pymap3d.geodetic2enu(targetInfo.lat,targetInfo.lon,targetInfo.h,moduleInfo.lat,moduleInfo.lon,moduleInfo.h))
     vector_enu = vector_enu/math.linalg.norm(vector_enu)
     
     #Rotates enu-centric vector to align to the axes of the module
     rotationMatrix = math.array([[math.cos(math.deg2rad(moduleInfo.heading)),-math.sin(math.deg2rad(moduleInfo.heading)),0],[math.sin(math.deg2rad(moduleInfo.heading)),math.cos(math.deg2rad(moduleInfo.heading)),0],[0, 0, 1]])
     vector_xyz = rotationMatrix.dot(vector_enu)
     #print str(vector_xyz)
     
     #Computes the two possible axes position solutions for the given pointing vector
     rotationSolution_1 = math.remainder(math.arctan2(vector_xyz[1],vector_xyz[0])*180/math.pi,360)
     elevationSolution_1 = math.remainder(math.arccos(vector_xyz[2])*180/math.pi,360)
     rotationSolution_2 = math.remainder(rotationSolution_1+180,360)
     elevationSolution_2 = math.remainder(360-elevationSolution_1,360)
     
     #Determines which solution is closer to the current state and sets it as the axes targets
     distanceToSolution_1 = math.linalg.norm(math.array([elevationAxis.getDistanceToTarget(elevationSolution_1), rotationAxis.getDistanceToTarget(rotationSolution_1)]))
     distanceToSolution_2 = math.linalg.norm(math.array([elevationAxis.getDistanceToTarget(elevationSolution_2), rotationAxis.getDistanceToTarget(rotationSolution_2)]))
     if distanceToSolution_1 < distanceToSolution_2:
       elevationTarget = elevationSolution_1
       rotationTarget = rotationSolution_1
     else:
       elevationTarget = elevationSolution_2
       rotationTarget = rotationSolution_2
     
     print "%%%%%%%"  
     print "Rotation target: " + str(round(rotationTarget,2)) + "deg, Elevation target: " + str(round(elevationTarget,2)) + "deg"
     print "%%%%%%%"
   
   #Moves the pointer towards its target (if told to)
   if (targetInfo.point and 2 < abs(max([elevationAxis.getDistanceToTarget(elevationTarget), rotationAxis.getDistanceToTarget(rotationTarget)],key=abs))):
     elevationAxis.point(elevationTarget)
     rotationAxis.point(rotationTarget)
     lastMoved = time.time()
   elif (time.time() - lastMoved > 20):
     elevationAxis.axisEncoder.getReading()
     rotationAxis.axisEncoder.getReading()
     lastMoved = time.time()
   time.sleep(0.1)
   
#Interrupt routine to safely close out of the program
except KeyboardInterrupt(): #sets up interrupt
  GPIO.cleanup() #cleanup of GPIO on control + c exit
  time.sleep(1)

#Closes out of program and shuts everything down on non-interrupt exit
GPIO.cleanup() #cleanup of GPIO on normal exit
