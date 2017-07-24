#!/usr/bin/env python3

import sys
import requests
import json
import subprocess
import platform
import psutil
import zipfile
#from flask import Flask, request
from datetime import datetime

server_ip = 'http://127.0.0.1:5000/'

program = 'telegram'

# get version of program you want to update
try:
	cmd = [program, "-version"]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
	out, err = p.communicate()
except FileNotFoundError:
	out = "0"

# send client data to server for first heartbeat
client_data = {"processor":platform.processor(), "platform":platform.platform(), "ram":(psutil.virtual_memory()[0])/1000000000, "name":platform.uname()[1], "date":datetime.now(), "program":program, "version":out}
print ("checking for update for " + program)
connection_return = requests.post(server_ip + "start_connection", data = client_data)

if(connection_return.text == 'no update available for this software'):
	print (connection_return.text)
else:
	print ('downloading update...')

	recieved_file = open(program + '.zip','wb') 
	recieved_file.write(connection_return.content)
	recieved_file.close() 

	print ('successfully downloaded update')
	print ('extracting update...')

	downloaded_zip = zipfile.ZipFile(program + '.zip')
	zipfile.ZipFile.extractall(downloaded_zip)