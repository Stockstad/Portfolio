from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
import data
import userman

app = Flask(__name__)
app.secret_key = 'very_secret'



@app.route('/', methods=['GET', 'POST'])
def index():
    session['db'] = data.load("test_data.json")
    session['dtek'] = []
    return render_template('index.html')

@app.route('/techniques')
def techniques():
    pl = session['db']
    techniques = data.get_techniques(pl)
    return render_template('techniques.html', techniques=techniques, dtek=session['dtek'])

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/list', methods=['POST', 'GET'])
def list():
    if request.method == 'GET':
        pl = session['db']
        techniques = data.get_techniques(pl)
        return render_template('list.html', pl=pl, techniques=techniques)
    else:
        pl = session['db']
        techniques = data.get_techniques(pl)
        search_key = request.form['text']
        sort_order = request.form.get('sortorder')
        sort_by = request.form.get('sortby')
        techs = request.form.getlist('techniques')

        print(str(sort_order))
        projects = data.search(db=pl, sort_by=sort_by, sort_order=sort_order, techniques=techs, search=search_key, search_fields=None)
        return render_template('list.html', projects=projects, techniques=techniques)






@app.route('/project/<int:project_id>')
def project(project_id):
    project = data.get_project(session['db'], project_id)
    if project == None:
        return "Project not found", 404
    
    return render_template('project.html', project=project)

@app.route('/process', methods=['POST'])
def process():
    res = request.get_json() # retrieve the data sent from JavaScript
    # process the data using Python code
    db = data.load("test_data.json")
    session['dtek'] = data.search(db=db, techniques=res)

    return jsonify(res=res) # return the result to JavaScript

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process login form data here
        username = request.form['username']
        password = request.form['password']

        # Implement authentication logic (e.g., check against a database)
        if userman.login(username, password):
            # Authentication successful, redirect to a protected page
            session['user'] = username
            return redirect(url_for('panel'))
        else:
            # Authentication failed, display an error messagecredentials
            error = 'Invalid credentials. Please try again.'
            return render_template('login.html', error=error)

    # If it's a GET request, just render the login form
    return render_template('login.html')

@app.route('/admin/panel', methods=['GET', 'POST'])
def panel():
    if request.method == 'POST':
        session.pop('user')
        return render_template('login.html')
    else:
        if 'user' in session:
            user = session['user']
            return render_template('panel.html', user=user)
        else:
            return redirect(url_for('login'))
                    



app.run(debug=True)

