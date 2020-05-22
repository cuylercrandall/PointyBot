import serial
from time import sleep
lineNumber = 0

#This code was an attempt to pull data from the GPS
#this code is written based on the code in write up reference 11
uart = serial.Serial ("/dev/ttyS0", 9600)
while True:
	recieved_data = uart.read()
	sleep(.03)
	data_left = uart.inWaiting()
	recieved_data += uart.read(data_left)
#	print(recieved_data)
	old_data = recieved_data
	length = len(old_data)
#	lineNumber = 0
	for x in range(4,(length-1)):
#		print(old_data[x])
#		print(old_data[x-1])
#		print(length)
		if ((old_data[x] == "G") and (old_data[x+1] == "G" )):
			print(length)
			print ("double g")
			startValue = x-4
			endValue = x+30
			lineOneValues=old_data[startValue: endValue]
			print(lineOneValues)
			lineNumber = 1
	if(lineNumber == 1):
		recieved_data = uart.read()
        	sleep(.03)
        	data_left = uart.inWaiting()
        	recieved_data += uart.read(data_left)
		lineTwoValues = recieved_data
		lineNumber = 2
		print(lineTwoValues)
	elif(lineNumber == 2):
		recieved_data = uart.read()
                sleep(.03)
                data_left = uart.inWaiting()
                recieved_data += uart.read(data_left)
		lineNumber = 0
		lineThreeValues = recieved_data
		print(lineThreeValues)




#def set_up_gps():
#     ser = serial.Serial(
#        port = '/dev/ttyAMA0',
#        baudrate = 9600,
#        parity = serial.PARITY_NONE,
#        stopbits = serial.STOPBITS_ONE,
#        bytesize = serial.EIGHTBITS,
#        timeout=1
#        )
#     counter=0
#     return ser
