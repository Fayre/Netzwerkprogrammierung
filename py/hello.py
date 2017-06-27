from flask import Flask, request, url_for, render_template, escape, redirect, session, jsonify
from datetime import datetime
app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#url_for('static', filename='style.css')

@app.route('/hello') # route tells Flask what URL should trigger our function
def hello_world():
    return 'Hello, World!' # message we want to display in the users browser


@app.route('/')
def index():
	#return render_template('index.html');
	if 'username' in session and 'ip' in session and 'date' in session:
		username = session['username']
		ip = session['ip']
		date = session['date']
		date_string = date.strftime('%d.%m.%Y %H:%M:%S')
		return 'Logged in as ' + username + '<br>' + \
		'IP: ' + ip + '<br>' + \
		'Date: ' + date_string + '<br>' + \
		"<b><a href = '/logout'>click here to log out</a></b>"
	return "You are not logged in <br><a href = '/login'></b>" + \
	"click here to log in</b></a>"


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		#session['ip'] = jsonify({'ip': request.remote_addr}), 200
		session['ip'] = request.environ['REMOTE_ADDR']
		session['date'] = datetime.now()
		# info contains CPU, GPU, RAM, ...		
		#session['info'] =
		return redirect(url_for('index'))
	return '''
	
	<form action = "" method = "post">
      <p><input type = text name = 'username' /></p>
      <p><input type = submit value = 'Login' /></p>
	</form> 
	'''

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('ip', None)
   return redirect(url_for('index'))


@app.route('/sessiontest')
def sessiontest():
	session['username'] = 'caro';
	return session['username'];
    #if 'username' in session:
    #    return 'Logged in as %s' % escape(session['username'])
    #return 'You are not logged in'
	

@app.route('/user/<username>') # visit e.g. http://[...]/user/caro to see Hello caro
def show_user_profile(username):
    # show the user profile for that user
    return 'Hello %s' % username


