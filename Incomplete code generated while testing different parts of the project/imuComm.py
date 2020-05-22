import FaBo9Axis_MPU9250

import time
import sys
import math

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

xscale = 26.62
yscale = 29.9915
xoffset = 19.416
yoffset = -7.4535

startTime = time.time()
magXSum = 0
magYSum = 0
counter = 0


#code is based off of the code in reference 1 and 3
while ((time.time()-startTime) < 15):
#	print("a")
	mag = mpu9250.readMagnet()
	magXSum = magXSum + mag['x']
	magYSum = magYSum + mag['y']
	counter = counter +1
	time.sleep(.05)


magXAve = magXSum/counter
magYAve = magYSum/counter
print  "average x =" , magXAve
print  "average y =" , magYAve

#magxoffset = ((magXAve*xscale) - xoffset)
#print  "offset x =" , magxoffset
#xcalc = ((magXAve - 670)/465)
xcalc = ((magXAve - 22)/20)
print "xcalc = " , xcalc
if ((xcalc < 1) and (xcalc > -1)):
	magx = math.acos(xcalc)
	print " mx = " ,  magx

#magyraw = mag['y']
#print "raw mag y =" , magyraw
#magyoffset = ((magYAve*yscale) - yoffset)
#print "offset y =" , magyoffset
ycalc = ((magYAve + 10)/18)
print "ycalc =" ,ycalc
if((ycalc < 1) and (ycalc > -1)):
	magy = math.asin(ycalc)
	print " my = " , magy

magz = mag['z']
