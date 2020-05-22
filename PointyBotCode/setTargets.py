# Kristina Nemeth (kan57) & Cuyler Crandall (csc254)
# ECE 5725 Final Project
#Functions that set the targetInfo.py to different targets (mainly static and dynamic ISS)

#General imports
import RPi.GPIO as GPIO
import os, time, threading
import numpy as math

#Specifically needed for these functions and ISS info
import moduleInfo, targetInfo, urllib2, json


#Writes the target file for a specified lat/lon/h
def writeTargetInfoFile(lat,lon,h,point,atISS):
  pythonOutput = open("/home/pi/PointyBot/PointyBotCode/targetInfo.py","w")
  pythonOutput.write("lat =" + str(lat) + "\n")
  pythonOutput.write("lon =" + str(lon) + "\n")
  pythonOutput.write("h =" + str(h) + "\n")
  pythonOutput.write("point =" + str(point) + "\n")
  pythonOutput.write("pointAtISS =" + str(atISS) + "\n")
  pythonOutput.close()    

#Starts pointing from not
def startPointing():
  import targetInfo
  writeTargetInfoFile(targetInfo.lat,targetInfo.lon,targetInfo.h,True)

#Stops motion
def stopPointing():
  import targetInfo
  writeTargetInfoFile(targetInfo.lat,targetInfo.lon,targetInfo.h,False)

#Sets targetInfo.py to current location of the ISS
def targetISS(externalCall=False):  
  #Reads current targetInfo file
  reload(targetInfo)
  
  doWrite = targetInfo.pointAtISS or externalCall
  
  #Polls ISS position API
  req = urllib2.Request("http://api.open-notify.org/iss-now.json")
  response = urllib2.urlopen(req)
  obj = json.loads(response.read())
  
  #print "Is currently targeting ISS: " + str(targetInfo.pointAtISS)
  #print "This is an external call: " + str(externalCall)
  
  #If it successfully got a new position, update the target file
  if (obj['message'] == "success" and doWrite) and externalCall: 
    writeTargetInfoFile(obj['iss_position']['latitude'],obj['iss_position']['longitude'],421.0*1000.0,targetInfo.point,True)
    reload(targetInfo)
  elif (obj['message'] == "success" and doWrite) and not externalCall:
    writeTargetInfoFile(obj['iss_position']['latitude'],obj['iss_position']['longitude'],421.0*1000.0,targetInfo.point,targetInfo.pointAtISS)
    reload(targetInfo)
  else:
    print "Failed to get ISS position, targetInfo.py not updated"
    
  #Starts timer to get new ISS position in 5 sec
  if targetInfo.pointAtISS:
    threading.Timer(5,targetISS).start()
  
#Sets target to ECE 5725 Lab
def pointAtLab():
  reload(targetInfo)
  writeTargetInfoFile(42.44427422,-76.48209304,244.0+20.0,targetInfo.point,False)
  reload(targetInfo)
  print str(targetInfo.pointAtISS)
  
#Sets target to Kristina's House
def pointAtKristina():
  reload(targetInfo)
  writeTargetInfoFile(26.1035208,-80.1172602,1.0,targetInfo.point,False)
  reload(targetInfo)
  print str(targetInfo.pointAtISS)
  
#Sets target to Cuyler's House
def pointAtCuyler():
  reload(targetInfo)
  writeTargetInfoFile(37.57853248,-122.35898763,13.0,targetInfo.point,False)
  reload(targetInfo)
  #print "Pointing at Cuylers House"
  print str(targetInfo.pointAtISS)
  
#Sets target to under the device (straight down)
def pointDown():
  reload(targetInfo)
  reload(moduleInfo)
  try:
    writeTargetInfoFile(moduleInfo.lat,moduleInfo.lon,moduleInfo.h-20.0,targetInfo.point,False)
  except:
    writeTargetInfoFile(moduleInfo.lat,moduleInfo.lon,moduleInfo.h-20.0,True,False)
  reload(targetInfo)
  print str(targetInfo.pointAtISS)
