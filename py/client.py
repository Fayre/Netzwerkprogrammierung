import sys
import requests
import json

server_ip = 'http://127.0.0.1:5000/hello_world'
post_data = {'name':'caro', 'hello':'world'}
server_return = requests.post(server_ip, data = post_data)

print (server_return.text)