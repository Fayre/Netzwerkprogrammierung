import sys
import requests
import json
import subprocess
import platform
import psutil
from datetime import datetime


server_ip = 'http://127.0.0.1:5000/'
post_data = {'name':'caro', 'hello':'world'}
server_return = requests.post(server_ip + "hello_world", data = post_data)

print (server_return.text)

#get current sysinfo based on os
#import sys
#if sys.platform == 'win32':
#	import win32_sysinfo as sysinfo
#elif sys.platform == 'darwin':
#	import mac_sysinfo as sysinfo
#elif 'linux' in sys.platform:
#	import linux_sysinfo as sysinfo


client_data = {"processor":platform.processor(), "ram":(psutil.virtual_memory()[0])/1000000000, "name":platform.uname()[1], "date":datetime.now()}
start_connection_return = requests.post(server_ip + "start_connection", data = client_data)

print (start_connection_return.text)


#print (platform.machine())
#print (platform.version())
#print (platform.platform())
#print (platform.processor())
#print (platform.system())
#print (platform.uname())
#print (psutil.cpu_percent())
#print ((psutil.virtual_memory()[0])/1000000000)

#cmd = ["wmic cpu get Name"]
#p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
#out, err = p.communicate()
#print (out)