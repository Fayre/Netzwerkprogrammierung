#!/usr/bin/env python3

from __future__ import print_function
from flask import Flask, request, session
from datetime import datetime
import platform
import json

"""
This is the server for the server-client-update-application.
If a client connects to this server, it checks for an update of the required software and if found, streams it to the client.
"""

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/start_connection', methods = ['POST'])
def start_connection():
	"""
	Starts the connection of server and client.
	In order to do so, stores everything in the session object. Starts the checking for update afterwards.
	"""
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


def check_for_update():
	"""
	Compares the current version of the program with the one stored on the server.
	Loads the data of the updates stored on the server as json string and compares it. If update is available, starts downloading it.
	"""
	with open('packages.json') as json_string:
		json_obj = json.load(json_string);

	if session['program'] not in json_obj:
		return 'no update available for this software'

	if session['version'] == json_obj[session['program']]['version']:
		return 'no update available for this software'
	else :
		return (get_update())

# searches for the update package
def get_update():
	"""
	Searches for update package.
	If found, stream it as binary to the client.
	"""
	with open('packages/' + session['program'] + '/' + session['program'] + '.zip', 'rb') as f:
		my_file = f.read()
	return my_file