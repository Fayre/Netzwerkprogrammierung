import sys
import requests
import json

server_ip = 'http://127.0.0.1:5000/hello_world'
server_return = requests.post(server_ip)

print (server_return.text)