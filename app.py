from flask import Flask, render_template, url_for
from flask_socketio import SocketIO, emit

import urllib
import RPi.GPIO as GPIO
import time
import json

CHANNEL_ID = "69826"
API_WRITE_KEY = 'IZAFZCYGRB0ZS3YU'
API_READ_KEY = 'D98FD7YB39AOLMMZ'

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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fabifarm2015!'
socketio = SocketIO(app)

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('server')
def server(msg):
	GPIO.output(switch1, 1)
	emit('client', {'data': 'hello'})

@socketio.on('settemperature')
def settemperature(temperature):
	params = urllib.urlencode({'key': API_WRITE_KEY, 'field3': temperature})
	f = urllib.urlopen("https://api.thingspeak.com/update", data=params)	

@socketio.on('setstarttime')
def setstarttime(starttime):
	params = urllib.urlencode({'key': API_WRITE_KEY, 'field4': starttime})
	f = urllib.urlopen("https://api.thingspeak.com/update", data=params)	

@socketio.on('setendtime')
def setendtime(endtime):
	params = urllib.urlencode({'key': API_WRITE_KEY, 'field5': endtime})
	f = urllib.urlopen("https://api.thingspeak.com/update", data=params)	

@socketio.on('server')
def server(msg):
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/3/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	targettemperature = parsed_response['field3']
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/4/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	starttime = parsed_response['field4']
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/5/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	endtime = parsed_response['field5']

	emit('client', {'targettemperature': targettemperature, 'starttime': starttime, 'endtime': endtime})

if __name__ == '__main__':
	socketio.debug = True
	socketio.run(app, host='0.0.0.0', port=80)
