#!/usr/bin/python
import sys
import urllib, urllib2
import json

API_WRITE_KEY = 'IZAFZCYGRB0ZS3YU'
API_READ_KEY = 'D98FD7YB39AOLMMZ'
URL = "fablabsaigon.ddns.net"
PORT = "8080"
AUTH_TOKEN = "047b8dc7a3674c17a990a96bdfc34fec"

# get temperature
jtemp = urllib2.urlopen("http://"+URL+":"+PORT+"/"+AUTH_TOKEN+"/pin/v10").read()
temperature = json.loads(jtemp)
print temperature[0]
# get humidity
jhumi = urllib2.urlopen("http://"+URL+":"+PORT+"/"+AUTH_TOKEN+"/pin/v11").read()
humidity = json.loads(jhumi)
print humidity[0]

if(temperature and humidity):
	params = urllib.urlencode({'key': API_WRITE_KEY, 'field1': temperature[0], 'field2': humidity[0]})
	f = urllib2.urlopen("https://api.thingspeak.com/update", data=params)
else:
	print 'Failed to get reading. Try again!'
	sys.exit(1)
