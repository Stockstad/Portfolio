from flask import Flask, render_template, request, redirect, url_for, flash, session
import data

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/techniques')
def techniques():
    return render_template('techniques.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/list')
def list():
    pl = data.load("test_data.json")
    return render_template('list.html', pl=pl)

@app.route('/project')
def project():
    return render_template('project.html')



app.run(debug=True)
