from flask import Flask, render_template, url_for, redirect
from flask_login import UserMixin
import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import json
from json import JSONEncoder

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecretkey'
bcrypt = Bcrypt(app)

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserEncoder(json.JSONEncoder):
    def default(self, o):
            return o.__dict__

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_name = getUser(username)
        if existing_user_name:
            return True
        return False

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/users/username')
def getUser(newUsername):
    return db.db.user.find({'username' : newUsername})

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    hashed_password = bcrypt.generate_password_hash(form.password.data)

    if form.validate_username(form.username.data):
        raise ValidationError(
            'That username already exists. Please choose a different one.')

    db.db.user.insert_one({'username':form.username.data, 'password':hashed_password})
    redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/test')
def test():
    db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"


if __name__ == '__main__':
    try:
        db.db.create_collection("user")
    except:
        pass
    app.run(debug=True, port=8000)
