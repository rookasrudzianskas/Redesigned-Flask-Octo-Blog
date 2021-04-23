from flask import Flask, render_template

# Create a flask appp

app = Flask(__name__)


# Create a new route
@app.route('/')
def index():
    return "<h1>Hello World</h1>"


# localhost:5000 🚀/user/rokas
@app.route('/user/<name>')
def user(name):
    return "<h1>Hello {} 🤜</h1>".format(name)
