from flask import Flask, render_template, request, redirect, url_for, flash, session

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
    p = {"Name": "TS-Project", "Course": "TDP007", "Tech": "C#, ASP.NET", "Link": "https//:rickroll.com"}
    return render_template('list.html', p=p['Name'])

@app.route('/project')
def project():
    return render_template('project.html')



app.run(debug=True)
