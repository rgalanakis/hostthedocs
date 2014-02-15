from flask import Flask, render_template

app = Flask(__name__)


@app.route('/hmfd')
def hmfd():
    pass

@app.route('/')
def home():
    return render_template('index.html', title='Welcome to Host the Docs')

