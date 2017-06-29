from flask import Flask, request, url_for, render_template, escape, redirect, session, jsonify
from datetime import datetime
import platform
import psutil

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#url_for('static', filename='style.css')

@app.route('/hello') # route tells Flask what URL should trigger our function
def hello_world():
    #return 'Hello, World!' # message we want to display in the users browser
	return render_template('index.html')


@app.route('/')
def index():
	#return render_template('index.html');
	if 'username' in session and 'ip' in session and 'date' in session:
		# get system info
		name = platform.uname()[1]
		processor = platform.processor()
		os = platform.platform()
		memory = psutil.virtual_memory()[1] /1000000000.0 # because return value is in byte

		info = [name, processor, os, memory]
		session['info'] = info

		# get session data
		username = session['username']
		ip = session['ip']
		date = session['date']
		date_string = date.strftime('%d.%m.%Y %H:%M:%S')
		return 'Logged in as ' + username + '<br>' + \
		'PC Name: ' + name + '<br>' + \
		'IP: ' + ip + '<br>' + \
		'Date: ' + date_string + '<br>' + \
		'Processor: ' + processor + '<br>' + \
		'Total Memory: ' + str(memory) + 'GB<br>' + \
		'Operating System: ' + os + '<br>' + \
		"<b><a href = '/logout'>click here to log out</a></b>"
	return "You are not logged in <br><a href = '/login'></b>" + \
	"click here to log in</b></a>"


def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['ip'] = request.environ['REMOTE_ADDR']
		session['date'] = datetime.now()
		# info contains CPU, GPU, RAM, ...
		#info = [0,1,2]
		#info[0] = request.form['cpu']
		#info[1] = request.form['gpu']
		#info[2] = request.form['ram']
		#session['info'] = info
		return redirect(url_for('index'))
	return render_template('login.html')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('ip', None)
   return redirect(url_for('index'))





#@app.route('/hardware_test')
#def hardware_test():
#	try:
#		cpu_genric_info = cpu_generic_details()
#	except Exception as ex:
#		print ex
#	finally:
#		return render_template("hardware_test_index.html", title="hardware_test_index", cpu_generic_info = cpu_generic_info)

#def cpu_generic_details():
#	try:
#		items = [s.split('\t: ') for s in subprocess.check_output(["cat /proc/cpuinfo | grep 'model name\|Hardware\|Serial' | uniq "], shell=True).splitlines()]
#	except Exception as ex:   
#		print ex
#	finally:
#		return items


