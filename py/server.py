#!/usr/bin/env python3

from __future__ import print_function
from flask import Flask, request, session
from datetime import datetime
import platform
import json


app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


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