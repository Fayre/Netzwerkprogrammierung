#!/usr/bin/env python3

from flask import Flask, Response
app = Flask(__name__)

@app.route("/")
def heartbeat():

	response = Response()
	response.headers['hello'] = "hello world"

	return response
