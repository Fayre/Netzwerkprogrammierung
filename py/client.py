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

# get version of program you want to update
cmd = ["firefox", "-version"]
p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
out, err = p.communicate()

# send client data to server for first heartbeat
client_data = {"processor":platform.processor(), "platform":platform.platform(), "ram":(psutil.virtual_memory()[0])/1000000000, "name":platform.uname()[1], "date":datetime.now(), "program":"firefox", "version":out}
#print ("checking for update for " + out)
print ("checking for update for ")
connection_return = requests.post(server_ip + "start_connection", data = client_data)

#zipfile.ZipFile.write('responsedata.zip', '')



print (connection_return.text)

recieved_file = open('responsedata.zip','wb') 
 
recieved_file.write(connection_return.content)
 
recieved_file.close() 


# check for update
#update_result = requests.post(server_ip + "check_for_update")
#print (update_result.text)



#print (platform.machine())
#print (platform.version())
#print (platform.platform())
#print (platform.processor())
#print (platform.system())
#print (platform.uname())
#print (psutil.cpu_percent())
#print ((psutil.virtual_memory()[0])/1000000000)
