#!/usr/bin/env python3
"""
This is the client for the server-client-update-application. 
It asks for the program to check and then starts a connection by sending all neccessary data to the server.
"""


import sys
import requests
import json
import subprocess
import platform
import psutil
import zipfile
from datetime import datetime


server_ip = 'http://127.0.0.1:5000/'

if(len(sys.argv) == 2):
	program = sys.argv[1]
else:
	print ("please enter the name of the software you want to update")
	sys.exit()

# get version of program you want to update
try:
	cmd = [program, "-version"]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
	out, err = p.communicate()
except (FileNotFoundError):
	out = "0"

# send client data to server for first heartbeat
client_data = {"processor":platform.processor(), "platform":platform.platform(), "ram":(psutil.virtual_memory()[0])/1000000000, "name":platform.uname()[1], "date":datetime.now(), "program":program, "version":out}
print ("searching for update for " + program)
connection_return = requests.post(server_ip + "start_connection", data = client_data)

if(connection_return.text == 'no update available for this software.' or connection_return.text == 'software is up to date.'):
	print (connection_return.text)
else:
	print ('update found.')
	print ('saving...')

	recieved_file = open(program + '.zip','wb') 
	recieved_file.write(connection_return.content)
	recieved_file.close() 

	print ('extracting update...')

	downloaded_zip = zipfile.ZipFile(program + '.zip')
	zipfile.ZipFile.extractall(downloaded_zip)

	print ('done - successfully downloaded update.')