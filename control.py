#!/usr/bin/python

import urllib
import datetime
import time
import json
import requests

CHANNEL_ID = "69826"
API_WRITE_KEY = "IZAFZCYGRB0ZS3YU"
API_READ_KEY = "D98FD7YB39AOLMMZ"
URL = "http://fablabsaigon.ddns.net:8080/047b8dc7a3674c17a990a96bdfc34fec/pin/"
HEADERS = {'content-type': "application/json"}

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

response = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/6/last.json?api_key=" + API_READ_KEY).read()
parsed_response = json.loads(response)
starttime2 = parsed_response['field6']
intstarttime2 = int(starttime2[0] + starttime2[1]) * 60 + int(starttime2[2] + starttime2[3])
#print intstarttime2

response = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/7/last.json?api_key=" + API_READ_KEY).read()
parsed_response = json.loads(response)
endtime2 = parsed_response['field7']
intendtime2 = int(endtime2[0] + endtime2[1]) * 60 + int(endtime2[2] + endtime2[3])
#print intendtime2

currentdatetime = datetime.datetime.now().time()
currenttime = currentdatetime.hour * 60 + currentdatetime.minute
#print currenttime

if (currenttime >= intstarttime and currenttime <= intendtime) or (currenttime >= intstarttime2 and currenttime <= intendtime2):
#	print 'In settime mode'
	requests.put(URL+"d5", data=json.dumps(["1"]), headers=HEADERS)
else:
	requests.put(URL+"d5", data=json.dumps(["0"]), headers=HEADERS)

#	print 'In auto mode'
if currenttemperature >= targettemperature:
	requests.put(URL+"d14", data=json.dumps(["1"]), headers=HEADERS)
	requests.put(URL+"d0", data=json.dumps(["1"]), headers=HEADERS)
	requests.put(URL+"d4", data=json.dumps(["1"]), headers=HEADERS)
else:
	requests.put(URL+"d14", data=json.dumps(["0"]), headers=HEADERS)
	requests.put(URL+"d0", data=json.dumps(["0"]), headers=HEADERS)
	requests.put(URL+"d4", data=json.dumps(["0"]), headers=HEADERS)
