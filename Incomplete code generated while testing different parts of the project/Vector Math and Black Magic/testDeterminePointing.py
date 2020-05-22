import RPi.GPIO as GPIO
import os
import time
import numpy as math
import pygeodesy
import pymap3d
import moduleInfo

#Adds physical escape button on TFT button
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([22, 27, 23, 17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins as inputs with pull up
#Defining callbacks for PiTFT buttons
def GPIO17_callback(channel):
  print("Button 17 (Quit) has been pressed")
  GPIO.cleanup()
  exit()
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)

myLat = 42.26
myLon = -76.28
myH = 186.4

testISSlat = -7.04
testISSlong = 7.86
testISSh = 421.0*1000.0

moduleLocation = pygeodesy.ecef.EcefCartesian(myLat,myLon,myH)
#print moduleLocation.toStr()
cartesianLoaction = moduleLocation.forward(testISSlat,testISSlong,testISSh)
#print cartesianLoaction.toStr()

vectorDirection = cartesianLoaction.toVector()
#print vectorDirection.toStr()

numpyDirection = math.array(vectorDirection)
#print str(round(math.linalg.norm(numpyDirection)/1000,2))
unitDirection = numpyDirection/math.linalg.norm(numpyDirection)
#print str(unitDirection)

rotationDirection = math.remainder(math.arctan2(unitDirection[1],unitDirection[0])*360/math.pi,360)
elevationDirection = math.remainder(math.arccos(unitDirection[2])*360/math.pi,360)

#print "Rotation Direction: " + str(round(rotationDirection,2))
#print "Elevation Direction: " + str(round(elevationDirection,2))

#Trying new package
vector = math.array(pymap3d.geodetic2enu(testISSlat,testISSlong,testISSh,myLat,myLon,myH))
print str(vector)
unitVector = vector/math.linalg.norm(vector)
rotationDirection = math.remainder(math.arctan2(unitVector[1],unitVector[0])*360/math.pi,360)
elevationDirection = math.remainder(math.arccos(unitVector[2])*360/math.pi,360)

print "Rotation Direction: " + str(round(rotationDirection,2))
print "Elevation Direction: " + str(round(elevationDirection,2))


while True:
  #print str(unitDirection)
  #print str(vectorDirection.x)
  #print str(vectorDirection/math.norm(vectorDirection))
  moduleInfo = reload(moduleInfo)
  print str(moduleInfo.lat)
  time.sleep(1)