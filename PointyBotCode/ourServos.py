# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project

import RPi.GPIO as GPIO
import time, threading, os
import numpy as math
import pigpio

##### Servo class
class servo:

  def __init__(self,servoPin,name):
    #os.system('sudo pigpiod')
    self.servoPin = servoPin
    self.name = name
    self.pi=pigpio.pi()
    #self.pi = pigpio.pi()
    #self.servo = GPIO.PWM(servoPin, 1)
    
    #Starts the servo (stopped)
    #self.servo.start(0)
    #self.servo.ChangeDutyCycle(0)
    self.pi.hardware_PWM(self.servoPin,800,0)

  def setServoSpeed(self,speed):
    if speed == 0:
      #self.servo.ChangeDutyCycle(0)
      self.pi.hardware_PWM(self.servoPin,800,0)
    else:#if speed >= -100 and speed <= 100:
		  #print str(speed)
		  #ms lengths of time for Parallax servo waveform
		  low_period = 20 #Low pulse
		  high_off = float(1.5) #High pulse length (ms) for no motion
		  #print str(float((speed*0.002)))
		  high_desired = high_off + float(0.002*speed)
		  #print "High time " + str(high_desired) + "ms"
	
		  #Convert to needed frequency and duty cycle
		  period = (low_period+high_desired)
		  frequency = 1000/period
		  #dutyCycle = 100*high_desired/period
		  dutyCycle = 255*high_desired/period
	
		  #Set PWM pin
		  #self.servo.ChangeFrequency(frequency)
		  #self.servo.ChangeDutyCycle(dutyCycle)
		  #self.pi.hardware_PWM(self.servoPin,frequency,dutyCycle)
		  self.pi.set_PWM_dutycycle(self.servoPin,dutyCycle)
		  self.pi.set_PWM_frequency(self.servoPin,frequency)
    #else:
		  #self.servo.stop()
		  #print "Requested speed outside of designated range, PWM cancelled"
        
  def stopServo(self):
    self.setServoSpeed(0)  
    
  def pulse(self,speed,time):
    self.setServoSpeed(speed)  
    threading.Timer(time,self.stopServo).start()
    #print "Pulsing " + self.name + " servo"
