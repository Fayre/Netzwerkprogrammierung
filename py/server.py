from flask import Flask, request, url_for, render_template, escape, redirect, session, jsonify
from datetime import datetime
import platform
import psutil
import subprocess

app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#url_for('static', filename='style.css')

@app.route('/')
def index():
	if 'username' in session and 'ip' in session and 'date' in session:
		# get system info
		name = platform.uname()[1]
		processor = platform.processor()
		#os = platform.platform()
		os = request.user_agent.platform
		memory = psutil.virtual_memory()[1] /1000000000.0 # because return value is in byte
		memory_str = str(memory)
		#gpu = get_available_gpus()		

		# info contains CPU, GPU, RAM, ...
		info = [processor, memory]
		session['info'] = info

		# get session data
		username = session['username']
		ip = session['ip']
		date = session['date']
		date_string = date.strftime('%d.%m.%Y %H:%M:%S')

		return render_template('home.html', username=username, name=name, ip=ip, date_string=date_string, processor=processor, memory=memory_str, os=os)
	return "You are not logged in <br><a href = '/login'></b>" + \
	"click here to log in</b></a>"


def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']


@app.route('/update', methods = ['GET', 'POST'])
def update():
	if 'username' in session and 'ip' in session and 'date' in session:
		browser = request.user_agent.browser
		version = request.user_agent.version and int(request.user_agent.version.split('.')[0])
		uas = request.user_agent.string
		prog_version = get_version("firefox")

		if request.method == 'POST':
			# update button pressed
			run_update("firefox")
			return render_template('update.html', current_state="updating...", browser=browser, version=version, uas=uas, prog_version=prog_version)

		return render_template('update.html', current_state="checking for updates...", browser=browser, version=version, uas=uas, prog_version=prog_version)
	return "You are not logged in <br><a href = '/login'></b>" + \
	"click here to log in</b></a>"


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		session['ip'] = request.environ['REMOTE_ADDR']
		session['date'] = datetime.now()
		
		return redirect(url_for('index'))
	return render_template('login.html')


@app.route('/logout')
def logout():
	# remove data from the session if it is there
	session.pop('username', None)
	session.pop('ip', None)
	session.pop('info', None)
	session.pop('date', None)
	return redirect(url_for('index'))


def get_version(program):
	cmd = [program, "-version"]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
	out, err = p.communicate()
	return out

def run_update(program):
	cmd = ["sudo", "apt-get", "update", "sudo", "apt-get", "install", program]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
	out, err = p.communicate()
	return out


@app.route('/test')
def test():
	cmd = ["firefox", "-version"]
	p = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
	out, err = p.communicate()
	return out


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


