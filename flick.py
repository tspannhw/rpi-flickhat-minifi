#!/usr/bin/env python
# -*- coding: <utf-8> -*-

# Based on
#Author: Callum Pritchard, Joachim Hummel
#Project Name: Flick 3D Gesture
#Project Description: Sending Flick 3D Gesture sensor data to mqtt
#Version Number: 0.1
#Date: 15/6/17
#Release State: Alpha testing
#Changes: Created

import time
import colorsys
import os
import json
import sys, socket
import subprocess
import time
import datetime
from time import sleep
from time import gmtime, strftime
import signal
import flicklib
import time
from curses import wrapper

some_value = 5000

flicktxt = ''

#### Initialization
# yyyy-mm-dd hh:mm:ss
currenttime= strftime("%Y-%m-%d %H:%M:%S",gmtime())

external_IP_and_port = ('198.41.0.4', 53)  # a.root-servers.net
socket_family = socket.AF_INET

host = os.uname()[1]

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

def IP_address():
        try:
            s = socket.socket(socket_family, socket.SOCK_DGRAM)
            s.connect(external_IP_and_port)
            answer = s.getsockname()
            s.close()
            return answer[0] if answer else None
        except socket.error:
            return None

def message(publisher, value):
    print value

@flicklib.move()
def move(x, y, z):
    global xyztxt
    xyztxt = '{:5.3f} {:5.3f} {:5.3f}'.format(x,y,z)

@flicklib.flick()
def flick(start,finish):
    global flicktxt
    flicktxt = 'FLICK-' + start[0].upper() + finish[0].upper()
    message('flick',flicktxt)

@flicklib.airwheel()
def spinny(delta):
    global some_value
    global airwheeltxt
    global flicktxt
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    airwheeltxt = str(some_value/100)
    flicktxt = airwheeltxt

@flicklib.double_tap()
def doubletap(position):
    global doubletaptxt
    global flicktxt
    doubletaptxt = position
    flicktxt = doubletaptxt

@flicklib.tap()
def tap(position):
    global taptxt
    global flicktxt
    taptxt = position
    flicktxt = taptxt

@flicklib.touch()
def touch(position):
    global touchtxt
    global flicktxt
    touchtxt = position
    flicktxt = touchtxt

def main():
    global xyztxt
    global flicktxt
    global airwheeltxt
    global touchtxt
    global taptxt
    global doubletaptxt

    flickcount = 0
    airwheeltxt = ''
    airwheelcount = 0
    touchtxt = ''
    touchcount = 0
    taptxt = ''
    tapcount = 0
    doubletaptxt = ''
    doubletapcount = 0

    time.sleep(0.1)

    while flickcount < 100:
        if (flicktxt != "") :
          flickcount += 100
	  cpuTemp=int(float(getCPUtemperature()))
          ipaddress = IP_address()
          row =  { 'ts': currenttime, 'host': host, 'cputemp': round(cpuTemp,2), 'ipaddress': ipaddress, 'flick': flicktxt }
          json_string = json.dumps(row)
          print(json_string)
	  sys.exit()

	time.sleep(0.1)
        flickcount += 1



main()
