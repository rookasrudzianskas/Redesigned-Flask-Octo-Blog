from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a flask appp

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key that no one knows"


# Create a form class

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a new route
@app.route('/')
# def index():
#     return "<h1>Hello World</h1>"
def index():
    first_name = "Rokas"
    favourite_pizza = ["Pepperoni", "margarita", "Rokas", "Cheese"]
    stuff = "This is <strong>Bold Text</strong>"
    return render_template('index.html',
                           first_name=first_name,
                           stuff=stuff,
                           favourite_pizza=favourite_pizza,
                           )


# localhost:5000 🚀/user/rokas
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)


# custom errror pages

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Create name page
@app.route('/name', methods=["GET", "POST"])
def name():
    name = None
    form = NameForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template("name.html",
                           name=name,
                           form=form,
                           )
