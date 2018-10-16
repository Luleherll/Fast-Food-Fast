from flask import Flask
from flask import request, redirect, render_template

app = Flask(__name__)


@app.errorhandler(404)
def not_found_error(e):
    return "<h1>You're lost in the woods:<br> Go back to index:<h1>\
<a href='https://lule-persistent.herokuapp.com/'>Click Here<a>", 404


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')