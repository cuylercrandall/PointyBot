#Kristina Nemeth (kan57) and Cuyler Crandall (csc254)
#PointyBot 4/19/2020

import RPi.GPIO as GPIO
import os
import time
from servoHelperFunctions import * #setServoSpeed #import helper function we created

elevationServoPin = 12
rotationServoPin = 13
servoSpeed = 100

#Adds physical escape button on TFT button
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([elevationServoPin, rotationServoPin], GPIO.OUT) #setup of LED pin from blink
GPIO.setup([22, 27, 23, 17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins as inputs with pull up resistors

#Defining callbacks for PiTFT buttons
def GPIO17_callback(channel):
  print("Button 17 (Quit) has been pressed")
  evelvationServo.stop()
  rotationServo.stop()
  GPIO.cleanup()
  exit()
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
def GPIO27_callback(channel):
  print("Button 27 (Reverse) has been pressed")
  setServoSpeed(evelvationServo,-servoSpeed)
  setServoSpeed(rotationServo,-servoSpeed)
GPIO.add_event_detect(27,GPIO.FALLING,callback=GPIO27_callback,bouncetime=300)
def GPIO23_callback(channel):
  print("Button 23 (Stop) has been pressed")
  setServoSpeed(evelvationServo,0)
  setServoSpeed(rotationServo,0)
GPIO.add_event_detect(23,GPIO.FALLING,callback=GPIO23_callback,bouncetime=300)
def GPIO22_callback(channel):
  print("Button 22 (Forward) has been pressed")
  setServoSpeed(evelvationServo,servoSpeed)
  setServoSpeed(rotationServo,servoSpeed)
GPIO.add_event_detect(22,GPIO.FALLING,callback=GPIO22_callback,bouncetime=300)

evelvationServo = startServo(elevationServoPin,0)
rotationServo = startServo(rotationServoPin,0)
timeStart = time.time()

#while loop used to keep code running so interrupts can be called by button presses
try:
  codeRunning = True
  while codeRunning:
    time.sleep(1)
except KeyboardInterrupt(): #sets up interrupt
  evelvationServo.stop()
  rotationServo.stop()
  GPIO.cleanup() #cleanup of GPIO on control + c exit
  time.sleep(1)
evelvationServo.stop()
rotationServo.stop()
GPIO.cleanup() #cleanup of GPIO on normal exit
