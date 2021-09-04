from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import date
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Create a flask appp

app = Flask(__name__)
# Add the database


# old sqllite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# new mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin1234@localhost/my_users'

app.config['SECRET_KEY'] = "my super secret key that no one knows"
# Initialize the database

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# this really works

# create a blog post model

# flask login stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# create a  login form

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')


# create login pages, to log in

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            # check the hashing
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfully")
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Password, try again :)')
        else:
            flash("That User Does not Exist, try again 🔥")
    return render_template("login.html", form=form)


# create log out
@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You have been Logged Out. :D")
    return redirect(url_for("login"))


# create dashboard page

@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():

    return render_template("dashboard.html")


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow())
    # something like adds _ to the url
    slug = db.Column(db.String(255))


#     create a post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


#     Add post page 🚀

@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        #     return the message to the
        flash("Blog Post was deleted successfully")
        # redirecting the user to the home
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template("posts.html", posts=posts)

    except:
        # the message
        flash("Whoops. There was a problem! Error: deleting failed successfully")
        posts = Posts.query.order_by(Posts.date_posted)
        # redirecting the user to the home
        return render_template("posts.html", posts=posts)


@app.route('/posts')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post=post)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data

        #         add to the database, update the

        db.session.add(post)
        db.session.commit()
        flash("Post has been updated 🚀")
        return redirect(url_for("post", id=post.id))

    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content

    return render_template("edit_post.html", form=form)


@app.route('/add-post', methods=["GET", "POST"])
# @login_required
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        # clear the form
        form.title.data = ""
        form.content.data = ""
        form.author.data = ""
        form.slug.data = ""

        #         add post data to db

        db.session.add(post)
        db.session.commit()

        # Return a message
        flash("Blog Post was Submitted Successfully")
    #         redirect
    return render_template("add_post.html", form=form)


# JSON everything
@app.route("/date")
def get_current_date():
    favourite_pizza = {
        "Rokas": "Margarita",
        "Mary": "Pepperoni",
        "Tim": "Vollcanion",

    }

    return favourite_pizza
    # return {"Date": date.today()}


# something


# Create the model for the database

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    data_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Do some password stuff
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not an readable Attribute!')

    # created setter to set the hashes
    @password.setter
    def password(self, password):
        # take whatever they type in the password field, and generate the hash
        # it takes the password which we enter to the modal, and pass it to the generate function, which generated the hash from it
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # this one verifies the password, if it is the correct one
        return check_password_hash(self.password_hash, password)

    #      Create a string
    def __repr__(self):
        return '<Name %r>' % self.name


# delete the user
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully 🚀!")
        our_users = Users.query.order_by(Users.data_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)
    except:
        flash("Whoops there was a problem deleting the user 💁‍♂️")
        our_users = Users.query.order_by(Users.data_added)
        return render_template('add_user.html', form=form, name=name, our_users=our_users)


# Create sign up form
class UserForm(FlaskForm):
    name = StringField("Name ✍️", validators=[DataRequired()])
    username = StringField("Username ✍️", validators=[DataRequired()])
    email = StringField("Email ✉️️", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    password_hash = PasswordField('Password', validators=[DataRequired(),
                                                          EqualTo('password_hash2', message="Passwords Must Match")])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField("Submit")


# update the database record

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    # checks if the user have submitted form
    if request.method == "POST":
        # the answer comes true, so the form name becomes the input field value of (name)
        name_to_update.name = request.form['name']
        #  the email becomes the email from the form
        name_to_update.email = request.form['email']
        # updates the color, the field added recently
        name_to_update.favorite_color = request.form['favorite_color']
        name_to_update.username = request.form["username"]
        try:
            # tries to update the user, if it updates, so the form gets refreshed and user redirected to update.htmls
            db.session.commit()
            # in the dictionary comes back the name_to_update which has .name and .email properties
            # we are going to use to put as the value, then entered /update/{{id}}, it puts the value to the inputs
            flash("updated Successfully! 🚀")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
        except:
            # if the error occurs, just returns to the same form with everything the same
            flash(" updated Unsuccessfully! 💁‍♂️")
            return render_template("update.html",
                                   form=form,
                                   name_to_update=name_to_update)
    # but if the request becomes the not the POST, the user does not press the submit button, or the form fails, so this means
    # the page will be refreshed to the same stage as it was before
    else:
        return render_template("update.html",
                               form=form,
                               name_to_update=name_to_update,
                               id=id)


class PasswordForm(FlaskForm):
    email = StringField("What is your email? ㊙️", validators=[DataRequired()])
    password = PasswordField("What is your password? ㊙️", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a form class

class NameForm(FlaskForm):
    name = StringField("What is your name? ㊙️", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods=["GET", "POST"])
def add_user():
    # name because first time there is no form name
    name = None
    # initializes users form
    form = UserForm()
    #  validates user form
    if form.validate_on_submit():
        # goes to the database users and gets the user which email is entered to the field and stores to users variable
        user = Users.query.filter_by(email=form.email.data).first()
        # is there is no user with that email, it creates the user with name and email to the users database
        if user is None:
            # Hash password
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            # outputing hashed one
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data,
                         favorite_color=form.favorite_color.data,
                         password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        #     sets the form name, then user is created or found in the db
        name = form.name.data
        # clears the form for another user
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash = ''
        flash("User added successfully")
    #     shows what is already added to the db
    our_users = Users.query.order_by(Users.data_added)
    return render_template('add_user.html', form=form, name=name, our_users=our_users)


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


# Create password test page
@app.route('/test_pw', methods=["GET", "POST"])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        form.email.data = ''
        form.password.data = ''
        # we are going to go per the users database and check if that email exists, then first one is found, we just return it
        pw_to_check = Users.query.filter_by(email=email).first()

        #     check hash password
        #  will return true or not
        passed = check_password_hash(pw_to_check.password_hash, password)
        print(passed)

    return render_template("test_pw.html",
                           email=email,
                           password=password,
                           pw_to_check=pw_to_check,
                           form=form,
                           passed=passed,
                           )


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

# login
