# create a  login form

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')


#     create a post form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")


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


class PasswordForm(FlaskForm):
    email = StringField("What is your email? ㊙️", validators=[DataRequired()])
    password = PasswordField("What is your password? ㊙️", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a form class

class NameForm(FlaskForm):
    name = StringField("What is your name? ㊙️", validators=[DataRequired()])
    submit = SubmitField("Submit")
