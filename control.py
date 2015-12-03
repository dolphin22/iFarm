#!/usr/bin/python

import urllib
import RPi.GPIO as GPIO
import datetime
import time
import json

CHANNEL_ID = "69826"
FIELD_ID = "1"
API_WRITE_KEY = "IZAFZCYGRB0ZS3YU"
API_READ_KEY = "D98FD7YB39AOLMMZ"

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

switch1 = 6
switch2 = 13
switch3 = 19
switch4 = 26
GPIO.setup(switch1, GPIO.OUT)
GPIO.setup(switch2, GPIO.OUT)
GPIO.setup(switch3, GPIO.OUT)
GPIO.setup(switch4, GPIO.OUT)

response = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/1/last.json?api_key=" + API_READ_KEY).read()
parsed_response = json.loads(response)
currenttemperature = parsed_response['field1']
#print currenttemperature

response = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/3/last.json?api_key=" + API_READ_KEY).read()
parsed_response = json.loads(response)
targettemperature = parsed_response['field3']
#print targettemperature

response = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/4/last.json?api_key=" + API_READ_KEY).read()
parsed_response = json.loads(response)
starttime = parsed_response['field4']
intstarttime = int(starttime[0] + starttime[1]) * 60 + int(starttime[2] + starttime[3])
#print intstarttime

response = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/5/last.json?api_key=" + API_READ_KEY).read()
parsed_response = json.loads(response)
endtime = parsed_response['field5']
intendtime = int(endtime[0] + endtime[1]) * 60 + int(endtime[2] + endtime[3])
#print intendtime

currentdatetime = datetime.datetime.now().time()
currenttime = currentdatetime.hour * 60 + currentdatetime.minute
#print currenttime

if currenttime >= intstarttime and currenttime <= intendtime:
#	print 'In settime mode'
	GPIO.output(switch1, 1)	
	GPIO.output(switch2, 1)	
	GPIO.output(switch3, 1)	
	GPIO.output(switch4, 1)	
else:
#	print 'In auto mode'
	if currenttemperature >= targettemperature:
		GPIO.output(switch1, 1)
		GPIO.output(switch2, 1)
		GPIO.output(switch3, 1)
		GPIO.output(switch4, 1)
	else:
		GPIO.output(switch1, 0)
		GPIO.output(switch2, 0)
		GPIO.output(switch3, 0)
		GPIO.output(switch4, 0)
