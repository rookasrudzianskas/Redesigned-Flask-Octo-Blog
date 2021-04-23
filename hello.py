from flask import Flask, render_template

# Create a flask appp

app = Flask(__name__)


# Create a new route
@app.route('/')
# def index():
#     return "<h1>Hello World</h1>"
def index():
    first_name = "Rokas"
    stuff = "This is <strong>Bold Text</strong>"
    return render_template('index.html',
                           first_name=first_name,
                           stuff=stuff,
                           )


# localhost:5000 🚀/user/rokas
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)
