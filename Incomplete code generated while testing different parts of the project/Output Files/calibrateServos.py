import pigpio
import time, threading, os
import numpy as math

def setServoSpeed(pi,pin,speed):
  if speed == 0:
    #self.servo.ChangeDutyCycle(0)
    pi.hardware_PWM(pin,800,0)
  else:#if speed >= -100 and speed <= 100:
    #print str(speed)
    #ms lengths of time for Parallax servo waveform
    low_period = 20 #Low pulse
    high_off = float(1.5) #High pulse length (ms) for no motion
    #print str(float((speed*0.002)))
    high_desired = high_off + float(0.002*speed)
    print "High time " + str(high_desired) + "ms"
	
    #Convert to needed frequency and duty cycle
    period = (low_period+high_desired)
    frequency = 1000/period
    #dutyCycle = 100*high_desired/period
    #dutyCycle = 1000000*high_desired/period
    dutyCycle = 255*high_desired/period	
 
		  #Set PWM pin
		  #self.servo.ChangeFrequency(frequency)
		  #self.servo.ChangeDutyCycle(dutyCycle)
    #pi.hardware_PWM(pin,frequency,dutyCycle)
    pi.set_PWM_dutycycle(pin,dutyCycle)
    pi.set_PWM_frequency(pin,frequency)

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
    elif speed >= -100 and speed <= 100:
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
		  #dutyCycle = 255*high_desired/period
		  dutyCycle = 1000000*high_desired/period
		  print str(period)
		  print str(frequency)
		  print str(dutyCycle)   
      
		  #Set PWM pin
		  #self.servo.ChangeFrequency(frequency)
		  #self.servo.ChangeDutyCycle(dutyCycle)
		  #self.pi.hardware_PWM(self.servoPin,frequency,dutyCycle)
		  self.pi.set_PWM_dutycycle(self.servoPin,dutyCycle)
		  self.pi.set_PWM_frequency(self.servoPin,frequency)
    else:
		  #self.servo.stop()
		  print "Requested speed outside of designated range, PWM cancelled"
        
  def stopServo(self):
    self.setServoSpeed(0)  
    
  def pulse(self,speed,time):
    self.setServoSpeed(speed)  
    threading.Timer(time,self.stopServo).start()
    #print "Pulsing " + self.name + " servo"

rotServo = servo(13,"Rot")
eleServo = servo(12,"Ele")

pi = pigpio.pi()
pi.hardware_PWM(12,800,0)
pi.hardware_PWM(13,800,0)


if True:
  try:
    #rotServo.setServoSpeed(0.0001)
    #eleServo.setServoSpeed(0.0001)
    #setServoSpeed(pi,13,0.0001)
    #setServoSpeed(pi,12,0.0001)
    
    #print "Stop"
    #time.sleep(10)
    
    #rotServo.pulse(100,0.1)
    #eleServo.pulse(100,0.1)
    
    #time.sleep(5)
    
    #rotServo.setServoSpeed(100)
    #eleServo.setServoSpeed(100)
    #setServoSpeed(pi,13,100)
    setServoSpeed(pi,12,100)
    
    time.sleep(10)
    
    #rotServo.setServoSpeed(-100)
    #eleServo.setServoSpeed(-100)
    #setServoSpeed(pi,13,-100)
    setServoSpeed(pi,12,-100)
    
    time.sleep(10)
    
    #rotServo.stopServo()
    #eleServo.stopServo()
    #setServoSpeed(pi,13,0)
    setServoSpeed(pi,12,0)
    
    #rotServo.setServoSpeed(0.0001)
    #eleServo.setServoSpeed(0.0001)
    #setServoSpeed(pi,13,0.0001)
    #setServoSpeed(pi,12,0.0001)
    
    #print "Stop"
    #time.sleep(10)
    
    #rotServo.pulse(100,0.1)
    #eleServo.pulse(100,0.1)
    
    #time.sleep(5)
    
    #rotServo.setServoSpeed(100)
    #eleServo.setServoSpeed(100)
    #setServoSpeed(pi,13,100)
    #setServoSpeed(pi,12,100)
    
    #time.sleep(5)
    
    #rotServo.setServoSpeed(-100)
    #eleServo.setServoSpeed(-100)
    #setServoSpeed(pi,13,-100)
    #setServoSpeed(pi,12,-100)
    
    #time.sleep(5)
    
    #rotServo.stopServo()
    #eleServo.stopServo()
    #setServoSpeed(pi,13,0)
    #setServoSpeed(pi,12,0)
    
  except:
    setServoSpeed(pi,12,0)
    setServoSpeed(pi,13,0)


if False:
#  try:
    gpioServo(12,1500)
    gpioServo(13,1500)
    
    time.sleep(5)
    
    gpioServo(12,1700)
    gpioServo(13,1700)
    
    time.sleep(5)
    
    gpioServo(12,1300)
    gpioServo(13,1300)
    
    time.sleep(5)
    
    setServoSpeed(pi,12,0)
    setServoSpeed(pi,13,0)
    
#  except:
#    setServoSpeed(pi,12,0)
#    setServoSpeed(pi,13,0)

if False:
 try:
   setServoSpeed(pi,12,0.0001)
   setServoSpeed(pi,13,0.0001)
 
   time.sleep(5)
   
   setServoSpeed(pi,12,100)
   setServoSpeed(pi,13,100)
   
   time.sleep(5)
   
   setServoSpeed(pi,12,-100)
   setServoSpeed(pi,13,-100)
   
   time.sleep(5)
   
   setServoSpeed(pi,12,0)
   setServoSpeed(pi,13,0)
 except:
   setServoSpeed(pi,12,0)
   setServoSpeed(pi,13,0)
   
exit()

pi.set_mode(13, pigpio.OUTPUT)
pi.set_mode(12, pigpio.OUTPUT)
print ("mode: ", pi.get_mode(13))
print("setting to: ",pi.set_servo_pulsewidth(13, 1500))
print("setting to: ",pi.set_servo_pulsewidth(12, 1500))
print("set to: ",pi.get_servo_pulsewidth(13))

time.sleep(5)

print("setting to: ",pi.set_servo_pulsewidth(13, 1700))
print("setting to: ",pi.set_servo_pulsewidth(12, 1700))

time.sleep(5)

print("setting to: ",pi.set_servo_pulsewidth(13, 1300))
print("setting to: ",pi.set_servo_pulsewidth(12, 1300))

time.sleep(5)

print("setting to: ",pi.set_servo_pulsewidth(13, 00))
print("setting to: ",pi.set_servo_pulsewidth(12, 00))
