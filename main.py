'''
SET UP INFO:
1. Install Python 3
2. CD into the directory
3. Run 'pip3 install Flask'
4. Run 'pip3 install pymongo' -- To be used soon
5. Run 'export FLASK_APP=main.py' or For windows: $env:FLASK_APP = "main.py" , or set FLASK_APP=main.py
6. Run 'python3 -m flask run'
7. Go to http://127.0.0.1:5000/ (or http://localhost:5000/) in your browser
8. Do ‘CTRL+C’ in your terminal to kill the instance.
9. To auto update the instance once you save ,export FLASK_DEBUG=1 or windows:  $env:FLASK_DEBUG = "main.py"
'''
from flask import Flask, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from Settings.App_Settings import SECRETKEY, TRACKMODIFICATIONS
from Settings.DB_Settings import dbuser,dbpass,dbhost,dbname


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRETKEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(dbuser,dbpass,dbhost,dbname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = TRACKMODIFICATIONS

db = SQLAlchemy()
db.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Classes
class User(db.Model,UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False,unique=True)
    password_hash = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.String(50), nullable=False)
    number_interactions = db.Column(db.Integer, nullable=False)

    def __init__(self, email, password_hash, name, date, phone_number, number_interactions):
        self.email = email
        self.full_name = name
        self.date_joined = date
        self.password_hash = password_hash
        self.phone_number = phone_number
        self.number_interactions = number_interactions

    def __repr__(self):
        return '<User %r>' % self.full_name


# Forms
class RegForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    name = StringField('name',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=0, max=20)])

class LogInForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
    
@app.route("/signup",methods=['GET','POST'])
def register_user():

    form = RegForm()
    if request.method == 'GET':

        return render_template('signup.html', form=form)

    elif request.method == 'POST':

        if form.validate_on_submit():
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email is not None:
                return render_template('signup.html', form=form, error="Email taken")  # We should return a pop up error msg as well account taken
            else:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                newUser = User(name=form.name.data, email=form.email.data,password_hash=hashpass,number_interactions=1,date=date.today(),phone_number="")
                db.session.add(newUser)
                db.session.commit()
                login_user(newUser)
                return redirect(url_for('landing_page'))
        return render_template('signup.html', form=form) #We should return a pop up error msg as well bad input

@app.route("/Login", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def Login():
    form = LogInForm()

    if request.method == 'GET':

        if current_user.is_authenticated == True:
            return redirect(url_for('landing_page'))
        return render_template('Login.html', form=form)

    elif request.method == 'POST':
        check_user = User.query.filter_by(email=form.email.data).first()
        if check_user:
            if check_password_hash(check_user['password'], form.password.data):
                login_user(check_user)
                return redirect(url_for('landing_page'))
            return render_template('Login.html', form=form, error="Incorrect password!")
        else:
            return render_template('Login.html', form=form, error="Email doesn't exist!")

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    try:
        del session['access_token']
    except Exception:
        pass
    return redirect("/login")

@app.route("/")
def landing_page():
    peter = User.query.filter_by(email='test3@testing.com').all()
    print(peter)
    return render_template('landing_page.html')


if __name__ == '__main__':
    app.run(debug=True)
