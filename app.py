from flask import Flask, render_template, url_for
from flask_login import UserMixin
import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_name = db.db.getUser(username)
        return

@app.route('/users/usrname')
def getUser(newUsername):
    return

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/test')
def test():
    db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"


if __name__ == '__main__':
    try:
        db.db.create_collection("user")
    except:
        pass
    try:
        user = {"username": "john", "password": "pass"}
        db.db.user.insertOne(user)
    except:
        print("eroare")
    app.run(debug=True, port=8000)
