from flask import Flask, render_template, request, redirect, url_for, flash, session
import data

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/techniques')
def techniques():
    pl = data.load("test_data.json")
    techniques = data.get_techniques(pl)
    return render_template('techniques.html', techniques=techniques)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/list')
def list():
    pl = data.load("test_data.json")
    techniques = data.get_techniques(pl)
    return render_template('list.html', pl=pl, techniques=techniques)

@app.route('/project')
def project():
    return render_template('project.html')



app.run(debug=True)
