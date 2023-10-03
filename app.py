from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from werkzeug.utils import secure_filename
import data
import userman
import json
import os
import uuid

UPLOAD_FOLDER = 'static'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER
app.secret_key = 'very_secret'



def get_file(file):
    # Generate a unique file name
    unique_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

# Save the file to the server
    file.save(file_path)

    return f"../static/{unique_filename}" 



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
        techs = request.form.getlist('technique')
        search_by = request.form.getlist('searchby')

        if len(search_by) < 1:
            search_by = None

        

        print(f"{search_key}, {sort_order}, {sort_by}, {techs}")

        projects = data.search(db=pl, sort_by=sort_by, sort_order=sort_order, techniques=techs, search=search_key, search_fields=search_by)
       
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
        print(username)
        print(password)
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
        name = request.form['project-name']
        course = request.form['course-name']
        start_date = request.form['start-date']
        end_date = request.form['end-date']
        techniques = request.form['tech-box'].split()
        repos_link = request.form['repo-link']
        desc = request.form['project-description']
        big_img = request.files['large-img']
        small_img = get_file(request.files['small-img'])


        session['db'] = data.load("test_data.json")
        
        new_project = {"name": name, "project_id": userman.generate_unique_id(session['db']), "course": course, "small_img": small_img, "big_img": None, "repos_link": repos_link, "techniques_used": techniques, "start_date": start_date, "end_date": end_date, "project_description": desc}

        session['db'].append(new_project)

        with open("test_data.json", "w") as file:
            json.dump(session['db'], file, indent=4)
        return render_template('panel.html', user=session['user'])
    else:
        return render_template('panel.html', user=session['user'])

app.run(debug=True)

