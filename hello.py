from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a flask appp

app = Flask(__name__)
# Add the database

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SECRET_KEY'] = "my super secret key that no one knows"
# Initialize the database

db = SQLAlchemy(app)


# Create the model for the database

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    data_added = db.Column(db.DateTime, default=datetime.utcnow)

    #      Create a string
    def __repr__(self):
        return '<Name %r>' % self.name


# Create sign up form
class UserForm(FlaskForm):
    name = StringField("Name ✍️", validators=[DataRequired()])
    email = StringField("Email ✉️️", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a form class

class NameForm(FlaskForm):
    name = StringField("What is your name? ㊙️", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods=["GET", "POST"])
def add_user():
    form = UserForm()
    return render_template('add_user.html', form=form)


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
        flash("Form was submitted successfully...")

    return render_template("name.html",
                           name=name,
                           form=form,
                           )
