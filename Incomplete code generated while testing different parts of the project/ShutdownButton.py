#Kristina Nemeth (kan57) and Cuyler Crandall (csc254)
#PointyBot 4/22/2020

import RPi.GPIO as GPIO
import os
import time

shutdownPin = 5

#Adds physical escape button on TFT button
GPIO.setmode(GPIO.BCM) #set up GPIO pins to broadcom setting
GPIO.setup([22, 27, 23, 17], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up GPIO pins on the TFT screen
GPIO.setup([shutdownPin], GPIO.IN, pull_up_down=GPIO.PUD_UP) #set up shutdown pin as an input

#Defining callbacks for PiTFT buttons
def GPIO17_callback(channel):
        print("Button 17 (Quit) has been pressed")
        GPIO.cleanup()
        exit()
GPIO.add_event_detect(17,GPIO.FALLING,callback=GPIO17_callback,bouncetime=300)
def GPIO5_callback(channel):
        print("Button 5 (Shutdown Pressed) has been pressed")
        print("Hold for 2 seconds to commence shutdown")
        time.sleep(2)
        if GPIO.input(shutdownPin) == 0:
          print("Shutting down")
          os.system("sudo shutdown -h now")
        else:
          print("Shutdown cancelled")
GPIO.add_event_detect(5,GPIO.FALLING,callback=GPIO5_callback,bouncetime=300)

#while loop used to keep code running so interrupts can be called by button presses
try:
        codeRunning = True
        while codeRunning:
                time.sleep(1)
except KeyboardInterrupt(): #sets up interrupt
        GPIO.cleanup() #cleanup of GPIO on control + c exit
	time.sleep(1)
GPIO.cleanup() #cleanup of GPIO on normal exit