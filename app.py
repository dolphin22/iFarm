#!/usr/bin/env python

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None

if async_mode is None:
    try:
        import eventlet
        async_mode = 'eventlet'
    except ImportError:
        pass

    if async_mode is None:
        try:
            from gevent import monkey
            async_mode = 'gevent'
        except ImportError:
            pass

    if async_mode is None:
        async_mode = 'threading'

    print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
    import eventlet
    eventlet.monkey_patch()
elif async_mode == 'gevent':
    from gevent import monkey
    monkey.patch_all()

from threading import Thread	
from flask import Flask, render_template, url_for, request, redirect, session
from flask_socketio import SocketIO, emit, disconnect

import flask.ext.login as flask_login

import urllib
import time
import json

CHANNEL_ID = "69826"
API_WRITE_KEY = 'IZAFZCYGRB0ZS3YU'
API_READ_KEY = 'D98FD7YB39AOLMMZ'

BLINK_URL = "http://fablabsaigon.ddns.net:8080"
BLINK_TOKEN = "047b8dc7a3674c17a990a96bdfc34fec"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'fabifarm2015!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users={'admin@ifarm.com':{'pw':'ifarmpw'}}

class User(flask_login.UserMixin):
	pass
	
@login_manager.user_loader
def user_loader(email):
	if email not in users:
		return
		
	user = User()
	user.id = email
	return user
	
@login_manager.request_loader
def request_loader(request):
	email = request.form.get('email')
	if email not in users:
		return
		
	user = User()
	user.id = email
	
	user.is_authenticated = request.form['pw'] == users[email]['pw']
	
	return user
	
@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

@app.route('/')
def index():
	if flask_login.current_user.is_authenticated:
		return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	
	email = request.form['email']
	if request.form['pw'] == users[email]['pw']:
		user = User()
		user.id = email
		flask_login.login_user(user)
		return redirect(url_for('home'))
		
	return 'Bad login'
	
@app.route('/home')
@flask_login.login_required
def home():
	return render_template('home.html')
	
@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect(url_for('index'))

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

@socketio.on('setstarttime2')
def setstarttime2(starttime):
	params = urllib.urlencode({'key': API_WRITE_KEY, 'field6': starttime})
	f = urllib.urlopen("https://api.thingspeak.com/update", data=params)	

@socketio.on('setendtime2')
def setendtime2(endtime):
	params = urllib.urlencode({'key': API_WRITE_KEY, 'field7': endtime})
	f = urllib.urlopen("https://api.thingspeak.com/update", data=params)	

@socketio.on('connect')
def connect_request():
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/3/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	targettemperature = parsed_response['field3']
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/4/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	starttime = parsed_response['field4']
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/5/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	endtime = parsed_response['field5']
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/6/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	starttime2 = parsed_response['field6']
	f = urllib.urlopen("http://api.thingspeak.com/channels/"+ CHANNEL_ID  +"/field/7/last.json?api_key=" + API_READ_KEY).read()
	parsed_response = json.loads(f)
	endtime2 = parsed_response['field7']
	
	emit('client', {'targettemperature': targettemperature, 'starttime': starttime, 'endtime': endtime, 'starttime2': starttime2, 'endtime2': endtime2})

@socketio.on('getswitches')
def getswitches():
	#f = urllib.urlopen(BLINK_URL + '/' + BLINK_TOKEN + '/pin/d14').read()
	#d14 = json.loads(f)[0]
	#f = urllib.urlopen(BLINK_URL + '/' + BLINK_TOKEN + '/pin/d0').read()
	#d0 = json.loads(f)[0]
	#f = urllib.urlopen(BLINK_URL + '/' + BLINK_TOKEN + '/pin/d4').read()
	#d4 = json.loads(f)[0]
	#f = urllib.urlopen(BLINK_URL + '/' + BLINK_TOKEN + '/pin/d5').read()
	#d5 = json.loads(f)[0]
	switches=["0","0","0","0"]
	emit('receiveswitches', {'switches': switches})

if __name__ == '__main__':
	socketio.run(app, debug=True, host='0.0.0.0', port=8080)