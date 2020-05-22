import RPi.GPIO as GPIO
import os
import time
import numpy as math
from ourEncoders import *
from ourServos import *
from ourAxes import *
import outputWiringConfig as config

#rotationServoPin = 13
#rotationEncoderChannel = 0
#elevationServoPin = 12
#elevationEncoderChannel = 1

#Adds physical escape button on TFT button
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([config.rotationServoPin,config.elevationServoPin], GPIO.OUT)
GPIO.setup([22, 27, 23, 17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins as inputs with pull up resistors
#Defining callbacks for PiTFT buttons
def GPIO17_callback(channel):
  print("Button 17 (Quit) has been pressed")
  GPIO.cleanup()
  exit()
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)

#rotationEncoder = encoder(rotationEncoderChannel,"Rotation")
#rotationServo = servo(rotationServoPin,"Rotation")
#elevationEncoder = encoder(elevationEncoderChannel,"Elevation")
#elevationServo = servo(elevationServoPin,"Elevation")

elevationAxis = axis(config.elevationServoPin,config.elevationEncoderChannel,"Elevation")
rotationAxis = axis(config.rotationServoPin,config.rotationEncoderChannel,"Rotation")

#elevationAxis.axisEncoder.calibrate()

targets = [0, 90, 180, 270]
target_index = 0

while True: 
  #rotationEncoder.getReading()
  #rotationEncoder.getReading()
  #rotationEncoder.getReading()
  #rotationServo.pulse(100,0.5)
  #elevationEncoder.getReading()
  #elevationEncoder.getReading()
  #elevationEncoder.getReading()
  #elevationServo.pulse(100,0.05)
  
  if True:
    #elevationTarget = math.random.randint(low=1, high=360)
    target = target_index #targets[target_index]
    print "Trying to point at " + str(round(target))
    
    #Setup if point() does not include looping
    #while abs(elevationAxis.axisEncoder.currentReading - elevationTarget) > 5:
      #print str(round(abs(elevationAxis.axisEncoder.currentReading - elevationTarget) ,2))
      #elevationAxis.point(elevationTarget)
      #time.sleep(0.05)
    
    while 2 < abs(max([elevationAxis.getDistanceToTarget(target), rotationAxis.getDistanceToTarget(target)],key=abs)):
      elevationAxis.point(target)
      rotationAxis.point(target)
      time.sleep(0.1)
    
    target_index = math.remainder(target_index+1,360)
    
  time.sleep(2)
    
  