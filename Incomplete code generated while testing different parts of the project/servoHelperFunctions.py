import RPi.GPIO as GPIO

#Sets up PWM on a selected pin and keeps it stopped
def startServo(servoPin,speed):
        servo = GPIO.PWM(servoPin, 1)
        servo.start(0)
        servo.ChangeDutyCycle(0)
	return servo

def setServoSpeed(servo,speed):
  if speed == 0:
    servo.ChangeDutyCycle(0)
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
		dutyCycle = 100*high_desired/period
	
		#Set PWM pin
		servo.ChangeFrequency(frequency)
		servo.ChangeDutyCycle(dutyCycle)
  else:
		servo.stop()
		speed = 0
		print "Requested speed outside of designated range, PWM cancelled"