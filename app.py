from bson import ObjectId
from flask import Flask, render_template, url_for, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import PySimpleGUI as sg

app = Flask(__name__)

app.config['SECRET_KEY'] = 'thisisasecretkey'
bcrypt = Bcrypt(app)

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    users = db.db.user
    user_json = users.find_one({'_id': ObjectId(user_id)})
    return User(user_json)

class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json

    # Overriding get_id is required if you don't have the id property
    # Check the source code for UserMixin for details
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/user/')
def getUser(newUsername):
    return db.db.user.find_one({'username' : newUsername})

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = getUser(form.username.data)
        if user:
            if bcrypt.check_password_hash(user['password'], form.password.data):
                loginuser = User(user)
                login_user(loginuser)
                return redirect(url_for('dashboard'))
            else:
                sg.Popup('Oops', 'Wrong password! Try again!')
    return render_template('login.html', form = form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        existing_user_name = User(getUser(form.username.data))
        if existing_user_name:
            sg.Popup('Username already exists!')

        else:
            db.db.user.insert_one({'username': form.username.data, 'password': hashed_password})
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    try:
        db.db.create_collection("user")
    except:
        pass
    app.run(debug=True, port=8000)
