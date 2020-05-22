# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project
# This file contains code that will calibrate the magnetometer.

#import python library for IMU
import FaBo9Axis_MPU9250

import time
import sys

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

#code is based on the code in write up references 3 and 1
#write data to a text file for reference
datafile =  open("calibrationData.txt", "w")
xmin = 32767
xmax = -32767

ymin = 32767
ymax = -32767

startTime = time.time()

#gather magnetometer data for thirty seconds
while (time.time() - startTime < 30):
	mag = mpu9250.readMagnet()

	magx = mag['x']
	magy = mag['y']
	print " mx = " ,  magx
	print " my = " ,  magy

#write data to file
	datafile.write("X")
	datafile.write(str(magx))
	datafile.write("Y")
	datafile.write(str(magy))
	datafile.write("\n")

#modify maximum and minimum values respectively if a value is greater than max or lower than min
	if (magx > xmax):
		xmax = magx
	if (magx < xmin):
	        xmin = magx
	if (magy > ymax):
                ymax = magy
	if (magy < ymin):
                ymin = magy

	time.sleep(0.25)

#print values and calculate offsets
print "Xmax = " + str(xmax) + ", Xmin = " + str(xmin) + ", Ymax = " + str(ymax) + ", Ymin = " + str(ymin)
xoffset = (xmax + xmin)/2
yoffset = (ymax + ymin)/2

print("offsetvalues")
print(xoffset)
print(yoffset)
datafile.write("offsetvalue x: ")
datafile.write(str(xoffset))
datafile.write("offsetvalue y : ")
datafile.write(str(yoffset))
datafile.write("\n")


print("scalevalues")
datafile.write("scalesetvalue x: ")
#datafile.write(str(xscale))
datafile.write("offsetvalue y : ")
#datafile.write(str(yscale))
datafile.write("\n")

#calculate scale value
xscaleA = (xmax - xmin)/2
yscaleA = (ymax - ymin)/2

print("scaleAvalues")
print(xscaleA)
print(yscaleA)
datafile.write("scaleAvalue x: ")
datafile.write(str(xscaleA))
datafile.write("offsetvalue y : ")
datafile.write(str(yscaleA))
datafile.write("\n")

datafile.close()

#infinite loop displaying values after calibration
while True:
	mag = mpu9250.readMagnet()
	magx = ((mag['x']*xscaleA) - xoffset)
        print " mx = " ,  magx
	magy = ((mag['y']*yscaleA) - yoffset)
        print " my = " , magy
	magz = mag['z']
        print " mz = " , ( mag['z'] )
	time.sleep(2)
