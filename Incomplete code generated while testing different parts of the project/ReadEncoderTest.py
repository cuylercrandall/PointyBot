#Kristina Nemeth (kan57) and Cuyler Crandall (csc254)
#PointyBot 4/22/2020

import RPi.GPIO as GPIO
import os
import time
import numpy as math

encoderPin = 12

#Adds physical escape button on TFT button
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([22, 27, 23, 17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins on the TFT screen
#Defining callbacks for PiTFT buttons
def GPIO17_callback(channel):
  print("Button 17 (Quit) has been pressed")
  GPIO.cleanup()
  exit()
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)

##### Encoder class
class encoder:

  def __init__(self, encoderPin):
    self.encoderPin = encoderPin

    GPIO.setup([self.encoderPin], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up encoder's pin as an input
    
    self.resetEncoder()

  def GPIOencoder_callback(self, channel):
    if GPIO.input(encoderPin) == 0:
      self.lowStart = time.time()
      self.dutyCycles.append(self.lowStart - self.highStart)
    elif GPIO.input(encoderPin) == 1:
      self.now = time.time()
      self.periods.append(self.highStart - self.now)
      self.highStart = self.now
      
  def GPIOencoderRising_callback(self, channel):
    self.now = time.time()
    self.periods.append(self.highStart - self.now)
    self.highStart = self.now
    
  def GPIOencoderFalling_callback(self, channel):
    self.now = time.time()
    self.dutyCycles.append(self.highStart - self.now)
    self.lowStart = self.now
      
  def resetEncoder(self):
    self.periods = []
    self.dutyCycles = []
    self.now = time.time()
    self.highStart = time.time()
    self.lowStart = time.time()
    
  def startEncoder(self):
    self.resetEncoder()
    GPIO.add_event_detect(self.encoderPin,GPIO.BOTH,self.GPIOencoder_callback,bouncetime=300)
    #GPIO.add_event_detect(self.encoderPin,GPIO.FALLING,self.GPIOencoderFalling_callback,bouncetime=300)
    #GPIO.add_event_detect(self.encoderPin,GPIO.RISING,self.GPIOencoderRising_callback,bouncetime=300)
    
  def stopEncoder(self):
    GPIO.remove_event_detect(self.encoderPin)
    
  def getEncoderReading(self):
#    try:
    #del self.periods[0]
    #del self.dutyCycles[0]
    print self.periods
    print self.dutyCycles
    meanPeriod = math.mean(self.periods)*1000 #ms
    meanDC = math.mean(self.dutyCycles)*100000/meanPeriod #%
    print("Mean period = "+str(int(meanPeriod))+"ms")
    print("Mean Duty Cycle = "+str(int(meanDC))+"%")
    print("%%%%%")
    

#while loop used to keep code running so interrupts can be called by button presses
try:
  codeRunning = True
  testEncoder = encoder(encoderPin)
  
  while codeRunning:
    testEncoder.startEncoder()
    time.sleep(2)
    testEncoder.stopEncoder()
    testEncoder.getEncoderReading()
        
except KeyboardInterrupt(): #sets up interrupt
  GPIO.cleanup() #cleanup of GPIO on control + c exit
  time.sleep(1)
GPIO.cleanup() #cleanup of GPIO on normal exit