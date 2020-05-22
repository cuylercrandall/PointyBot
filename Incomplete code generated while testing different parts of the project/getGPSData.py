import serial
import time
from time import sleep
lineNumber = 0

datafile =  open("gpsData.txt", "w")
uart = serial.Serial ("/dev/ttyS0", 9600)
startTime = time.time()


#this is written based on the code in reference 11
while (time.time() - startTime < 1.5):
	recieved_data = uart.read()
	sleep(.03)
	data_left = uart.inWaiting()
	recieved_data += uart.read(data_left)
	datafile.write(recieved_data)

datafile.close()
gpsInfo = open("gpsData.txt", "r")
GPS = gpsInfo.read()
listLength = len(GPS)
index = 0;

for i in range(listLength-1):
	if ((GPS[i] == "G") and (GPS[i+1] == "G" )):
		print("double g")
		x = i


latitude = GPS[x+14]+GPS[x+15]+GPS[x+16]+GPS[x+17]
lat = (float(latitude)/100)
latsign = GPS[x+25]
longitude = GPS[x+28]+GPS[x+29]+GPS[x+30]+GPS[x+31]
lonsign = GPS[x+39]
lon = (float(longitude)/100)
height = GPS[x+51]+GPS[x+52]+GPS[x+53]+GPS[x+55]
h = (float(height)/10)

if((latsign == "S") or (latsign == "W")):
	lat = lat*(-1)
if((lonsign == "S") or (lonsign == "W")):
        lon = lon*(-1)

#print(lat)
#print(latsign)
#print(lon)
#print(lonsign)
#print(h)

gpsInfo.close()

pythonOutput = open("PointyBotCode/moduleInfo.py","w")
pythonOutput.write("lat =" + str(lat) + "\n")
pythonOutput.write("lon =" + str(lon) + "\n")
pythonOutput.write("h =" + str(h) + "\n")
pythonOutput.close()
