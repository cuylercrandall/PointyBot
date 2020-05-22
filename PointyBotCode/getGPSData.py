# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project
# This file is responsible for the gathering and processoing of GPS data.
# The data is then written to the module infomation

import serial
import time
from time import sleep

def getGPSData(iterateCount = 0):
	lineNumber = 0

	datafile =  open("gpsData.txt", "w")

	#Uart connection is set up - based on code in write up reference 11
	uart = serial.Serial ("/dev/ttyS0", 9600)
	startTime = time.time()

	#Uart data is saved and read to file for 3 seconds
	while (time.time() - startTime < 3):
		recieved_data = uart.read()
		sleep(.03)
		data_left = uart.inWaiting()
		recieved_data += uart.read(data_left)
		datafile.write(recieved_data)

	datafile.close()
	gpsInfo = open("gpsData.txt", "r")
	#gps data is saved to a list
	GPS = gpsInfo.read()
	listLength = len(GPS)
	index = 0;
	default = False;
	#list is parsed to find the location of GPGGA data by looking for the index of the first g
	for i in range(listLength-1):
		if ((GPS[i] == "G") and (GPS[i+1] == "G" )):
		#	print("double g")
			x = i

	try:
		#separate out the degree, degree minute and degree second
		latitudeDegree = GPS[x+14]+GPS[x+15]
		latitudeFirstAngle = GPS[x+16]+GPS[x+17]
		latitudeSecondAngle = GPS[x+19]+GPS[x+20]
		#convert to decimal degrees
		latitudeFirstAngleFloat = (float(latitudeFirstAngle)/60)
		latitudeSecondAngleFloat = (float(latitudeSecondAngle)/3600)
		lat = (float(latitudeDegree)+latitudeFirstAngleFloat+latitudeSecondAngleFloat)
		latsign = GPS[x+25]
		print latitudeFirstAngle
		print latitudeSecondAngle
		print str(latitudeFirstAngleFloat)
		print str(latitudeSecondAngleFloat)
		print "Lat = " + str(lat)

		#separate out the degree, degree minute and degree second
		longitudeDegree = GPS[x+28]+GPS[x+29]
		longitudeFirstAngle = GPS[x+30]+GPS[x+31]
                longitudeSecondAngle = GPS[x+33]+GPS[x+34]
		#convert to decimal degrees
		longitudeFirstAngleFloat = (float(longitudeFirstAngle)/60)
                longitudeSecondAngleFloat = (float(longitudeSecondAngle)/3600)
                lon = (float(longitudeDegree)+longitudeFirstAngleFloat+longitudeSecondAngleFloat)
		print "Lon = " + str(lon)
		lonsign = GPS[x+39]

		#get height data
		height = GPS[x+51]+GPS[x+52]+GPS[x+53]+GPS[x+55]
		h = (float(height)/10)


		#change sign of latitude and longitude to negative dependent on sign
		if((latsign == "S") or (latsign == "W")):
			lat = lat*(-1)
		if((lonsign == "S") or (lonsign == "W")):
	        	lon = lon*(-1)

		#write data to moduleInfo.py
	  	pythonOutput = open("moduleInfo.py","w")
	  	pythonOutput.write(str(default) + "\n")
	  	pythonOutput.write("lat = " + str(lat) + "\n")
	  	pythonOutput.write("lon = " + str(lon) + "\n")
	  	pythonOutput.write("h = " + str(h) + "\n")
	  	pythonOutput.write("heading = " + str(0.00) + "\n") 
	  	pythonOutput.close()

	#sometimes the GPS data does get picked up properly which causes errors in the previous lines, this allows the error to get caught
	except:
		iterateCount = iterateCount + 1
		if iterateCount < 5:
			getGPSData(iterateCount)
		else:
			default = True
 			lat =  42.4407
			lon = -76.4827
			h = 186.4
			#write a default value
			pythonOutput = open("moduleInfo.py","w")
			pythonOutput.write(str(default) + "\n")
			pythonOutput.write("lat = " + str(lat) + "\n")
			pythonOutput.write("lon = " + str(lon) + "\n")
			pythonOutput.write("h = " + str(h) + "\n")
			pythonOutput.write("heading = " + str(0.00) + "\n") 
			pythonOutput.close()


#print(lat)
#print(latsign)
#print(lon)
#print(lonsign)
#print(h)

	gpsInfo.close()

