from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
import data

app = Flask(__name__)
app.secret_key = 'very_secret'


@app.route('/', methods=['GET', 'POST'])
def index():
    session['dtek'] = []
    return render_template('index.html')

@app.route('/techniques')
def techniques():
    pl = data.load("test_data.json")
    techniques = data.get_techniques(pl)
    return render_template('techniques.html', techniques=techniques, dtek=session['dtek'])

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/list')
def list():
    pl = data.load("test_data.json")
    techniques = data.get_techniques(pl)
    return render_template('list.html', pl=pl, techniques=techniques)


@app.route('/list', methods=['GET', 'POST'])
def list_post():
    pl = data.load("test_data.json")
    techniques = data.get_techniques(pl)

    text = request.form['text']
    text = text.lower()
    if text == "":
        text = None

   
    orderbuttons = request.form.get("sortby")
    #reqorder = orderbuttons['sortby']

    #buttons = request.form['checkbox']
    projects = data.search(pl, sort_by="project_id", sort_order="asec", techniques=[], search=text, search_fields=None)

    return orderbuttons
    #return render_template('list.html',pl=projects, techniques=techniques)


#@app.route('/formsub', methods=['POST'])
#def formsub():
#    orderbuttons = request.form.get('sortby')
#    print(orderbuttons)
#    return orderbuttons


@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/process', methods=['POST'])
def process():
    res = request.get_json() # retrieve the data sent from JavaScript
    # process the data using Python code
    db = data.load("test_data.json")
    session['dtek'] = data.search(db=db, techniques=res)

    return jsonify(res=res) # return the result to JavaScript



app.run(debug=True)
