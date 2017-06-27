from flask import Flask, request, url_for, render_template
app = Flask(__name__)
#url_for('static', filename='style.css')

@app.route('/hello') # route tells Flask what URL should trigger our function
def hello_world():
    return 'Hello, World!' # message we want to display in the users browser


@app.route('/')
def index_hello():
	return render_template('index.html');
	

@app.route('/user/<username>') # visit e.g. http://[...]/user/caro to see Hello caro
def show_user_profile(username):
    # show the user profile for that user
    return 'Hello %s' % username


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)



# http://flask.pocoo.org/docs/0.12/quickstart/#quickstart  -  the request object
