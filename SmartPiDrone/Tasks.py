#####################################
#   File Name : PiDrone.py   
#   Author      : NayLA  
#   Date         : 11/03/2017
#####################################
from threading import Thread
import RPi.GPIO as GPIO
import sys
import time
import thread
import datetime
from UltrasonicSensor import *
import Adafruit_DHT
from Server import *
from DroneData import *


def DummyThread(param):
    while 1:
        print("Dummy Thread running....\r\n")
        time.sleep(param)

def MavLinkSerialCommThread(commdata):
    while 1:
        commdata.parseParameters()
        time.sleep(1)


def ReceiveControlCmdThread(cmdreceiver):
    while 1:
        print("Receiving Control command from App....\r\n")
        cmdreceiver.getCmd()
        time.sleep(2)

def performOperation(cmdexecutor,cmd):
    while 1:
        print("Executing command on drone....\r\n")
        cmdexecutor.executeCmd(cmd)
        time.sleep(2)


def Sonar1Thread(sonar_object):
    while 1:
        global cycle
        #print("Getting ultrasonic sensor-1  data....\r\n")
        print("Sonar-1 :  %s" %sonar_object.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.1)

def Sonar2Thread(sonar_object):
    while 1:
        global cycle
        #print("Getting ultrasonic sensor-2  data....\r\n")
        print("Sonar-2 :  %s" %sonar_object.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.1)

def Sonar3Thread(sonar_object):
    while 1:
        global cycle
        #print("Getting ultrasonic sensor-3  data....\r\n")
        print("Sonar-3 :  %s" %sonar_object.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.1)

def Sonar4Thread(sonar_object):
    while 1:
        global cycle
        #print("Getting ultrasonic sensor-4  data....\r\n")
        print("Sonar-4 :  %s" %sonar_object.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.1)

def HumidityAM2302Thread(hud_sensor):
    while 1:
        # Try to grab a sensor reading.  Use the read_retry method which will retry up
        # to 15 times to get a sensor reading (waiting 2 seconds between each retry).
        humidity, temperature = Adafruit_DHT.read_retry(hud_sensor, 25)

        # Note that sometimes you won't get a reading and
        # the results will be null (because Linux can't
        # guarantee the timing of calls to read the sensor).  
        # If this happens try again!
        if humidity is not None and temperature is not None:
            print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
        else:
            print 'Failed to get reading. Try again!'
        time.sleep(2)


def GetAllSensorDataThread(s1,s2,s3,s4,DHT_AM2302):
    while 1:
        print("Getting all data.....\r\n")
        HumidityAM2302Thread(DHT_AM2302)
        print("Sonar-1 :  %s" %s1.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.2)
        print("Sonar-2 :  %s" %s2.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.2)
        print("Sonar-3 :  %s" %s3.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.2)
        print("Sonar-4 :  %s" %s4.raw_distance(sample_size=7,sample_wait=0.1))
        time.sleep(0.2)


def SocketServeContinuousThread(server, dicData, timestamp ,delay):
     while 1:
        server.ServeContinuously(dicData ,timestamp)
        time.sleep(delay)
         

def SocketServerThread(server, dicData, timestamp ,delay):
    while 1:
        server.waitForConnection()
        server.serviceToClient(dicData ,timestamp)
        time.sleep(delay)
