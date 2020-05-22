import RPi.GPIO as GPIO
import numpy as math
import os, time, threading
from ourEncoders import *
from ourServos import *
#import outputConfig

##### Axis class
class axis:

  def __init__(self,servoPin,encoderPort,name):
    self.axisServo = servo(servoPin,name)
    self.axisEncoder = encoder(encoderPort,name)
    self.name = name
    
    self.orientation = self.getOrientation()
    
  #Stops the axis
  def stopAxis(self):
    self.servo.stop
  
  def getOrientation(self):
    #Pulses servo in one direction twice (collecting three encoder readings)
    self.axisServo.pulse(100,0.25)
    time.sleep(2)
    self.axisEncoder.clearEncoder()
    initialReading = self.axisEncoder.getReading()
    self.axisEncoder.clearEncoder()
    self.axisServo.pulse(100,0.25)
    time.sleep(2)
    secondReading = self.axisEncoder.getReading()
    self.axisEncoder.clearEncoder()
    self.axisServo.pulse(100,0.25)
    time.sleep(2)
    thirdReading = self.axisEncoder.getReading()
    
    
    #Checks that the three readings are increasing or decreasing and saves that info
    #Else tries again (in case it hits the 360 to 0 overflow
    if initialReading < secondReading and secondReading < thirdReading:
      print "Positive Orientation"
      return 1
    elif initialReading > secondReading and secondReading > thirdReading:
      print "Reversed Orientation"
      return -1
    else:
      return self.getOrientation()
  
  #Orients axis to target degrees on the encoder  
  def point(self,target):
    
    distance_to_target = self.getDistanceToTarget(target)
    
    #If sufficient distance away, move towards target
    if abs(distance_to_target) > 2: #abs(target - self.axisEncoder.currentReading) > 2:
      
      #Uncommenting this while loop will cause the axis to loop until it is pointed in the desired direction
      #Keeping it commented will perform only a single step (ie. to control both simultaneously) 
      #while abs(distance_to_target) > 1: #abs(target - self.axisEncoder.currentReading) > 1:
      if True:
      
        #Now that the direction is set, begin moving in that direction, updating encoder until there
        if self.name == "Rotation":
          pulseLength = 0.025+(distance_to_target/400)**2
        else:
          pulseLength = 0.05+(distance_to_target/400)**2#+(distance_to_target/100)**2
        pulseStart = time.time()
        #self.axisServo.pulse(self.orientation*direction*100,0.05)
        self.axisServo.pulse(self.orientation*math.sign(distance_to_target)*50,pulseLength)
        time.sleep(max([0,time.time()-pulseStart-pulseLength]))
        self.axisEncoder.getReading()
        #time.sleep(0.1)
        
        #Recalculate distance error
        distance_each_direction = [math.remainder(target-self.axisEncoder.currentReading,360), math.remainder(self.axisEncoder.currentReading-target,360)]
        distance_to_target = min(distance_each_direction, key=abs)
        
      #Run again to account for overshoot (just in case, shoudl hit the else statement below this only)
      #Clears encoder readings just in case
      #self.axisEncoder.clearEncoder()
      #self.axisEncoder.getReading()
      #self.axisEncoder.getReading()
      #self.point(target)
    
    #Else statement confirms on-target  
    else:
      print "Pointing at " + str(round(target,2)) + "deg (actual " + str(round(self.axisEncoder.currentReading,2)) + "deg)"
      
  #Determines signed distance from the target
  def getDistanceToTarget(self,target):
    distance_each_direction = [math.remainder(target-self.axisEncoder.currentReading,360), math.remainder(self.axisEncoder.currentReading-target,360)]
    
    if distance_each_direction[0] < distance_each_direction[1]:
      return min(distance_each_direction, key=abs)
    else:
      return -1*min(distance_each_direction, key=abs)
  
      