#!/usr/bin/env python3

from __future__ import print_function
from flask import Flask, request, url_for, render_template, escape, redirect, session, jsonify, send_file, send_from_directory
from datetime import datetime
import platform
#import psutil
import subprocess
import sys
import json
import requests
import zipfile


app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#SESSION_TYPE = 'redis'
#app.config.from_object(__name__)
#Session(app)
#app.run(host='0.0.0.0')

@app.route('/')
def index():
	if 'username' in session and 'ip' in session and 'date' in session:
		# get system info
		name = platform.uname()[1]
		processor = platform.processor()
		#os = platform.platform()
		os = request.user_agent.platform
		#memory = psutil.virtual_memory()[1] /1000000000.0 # because return value is in byte
		memory = 100;
		memory_str = str(memory)
		#gpu = get_available_gpus()		

		# info contains CPU, GPU, RAM, ...
		info = [processor, memory]
		session['info'] = info

		# get session data
		username = session['username']
		ip = session['ip']
		date = session['date']
		date_string = date.strftime('%d.%m.%Y %H:%M:%S')

		return render_template('home.html', username=username, name=name, ip=ip, date_string=date_string, processor=processor, memory=memory_str, os=os)
	return "You are not logged in <br><a href = '/login'></b>" + \
	"click here to log in</b></a>"

# not working yet
def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']


@app.route('/update', methods = ['GET', 'POST'])
def update():
	if 'username' in session and 'ip' in session and 'date' in session:
		browser = request.user_agent.browser
		version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
		uas = request.user_agent.string
		
		program_to_check = "firefox"
		prog_version = get_version(program_to_check)
		
		# check if update is available
		update_is_available = check_for_update(program_to_check, "54.0.0")

		if request.method == 'POST':
			# update button pressed
			#run_update(program_to_check)
			return render_template('update.html', current_state="update complete!", browser=browser, version=version, uas=uas, prog_version=prog_version, update_is_available=update_is_available)

		return render_template('update.html', current_state="check for updates", browser=browser, version=version, uas=uas, prog_version=prog_version, update_is_available=update_is_available)
	return "You are not logged in <br><a href = '/login'></b>" + \
	"click here to log in</b></a>"


# return 0 for false: no update
# return 1 for true: update available
def check_for_update(program, prog_version):

	with open('packages.json') as json_string:
		json_obj = json.load(json_string);

	if program == "firefox" and prog_version == json_obj["firefox"]["version"]:
		return 0
	return 1

@app.route('/download_update')
def run_update():
	try:
		return send_file('packages/firefox/firefox-54.0.1.tar.bz2', attachment_filename='firefox-54.0.1.tar.bz2')
	except Exception as e:
		return str(e)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['ip'] = request.environ['REMOTE_ADDR']
		session['date'] = datetime.now()
		
		return redirect(url_for('index'))
	return render_template('login.html')


@app.route('/logout')
def logout():
	# remove data from the session if it is there
	session.pop('username', None)
	session.pop('ip', None)
	session.pop('info', None)
	session.pop('date', None)
	return redirect(url_for('index'))


def get_version(program):
	cmd = [program, "-version"]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
	out, err = p.communicate()
	return out


@app.route('/test')
def test():
	cmd = ["firefox", "-version"]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
	out, err = p.communicate()
	return out
	
#---------------------------------------------------------------------

@app.route('/hello_world', methods = ['POST'])
def hello_world():
	#return request.form['data']
	data = request.form['name']
	return "access granted"


@app.route('/start_connection', methods = ['POST'])
def start_connection():
	# setup data
	session['name'] = request.form['name']
	session['date'] = request.form['date']
	session['ip'] = request.remote_addr
	session['processor'] = request.form['processor']
	session['ram'] = request.form['ram']
	session['platform'] = request.form['platform']
	session['program'] = request.form['program']
	session['version'] = request.form['version']
	return (check_for_update())


# return 0 for false: no update
# return 1 for true: update available
def check_for_update():
	with open('packages.json') as json_string:
		json_obj = json.load(json_string);

	if session['program'] not in json_obj:
		return 'no update available for this software'

	if session['version'] == json_obj[session['program']]['version']:
		return "no update"
	else :
		return (get_update())

# searches for the update package
def get_update():
	with open('packages/' + session['program'] + '/' + session['program'] + '.zip', 'rb') as f:
		my_file = f.read()
	return my_file