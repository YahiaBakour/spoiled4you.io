from flask import Flask, render_template, request,redirect,url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateTimeField, TextAreaField
from wtforms.validators import Email, Length, InputRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from Util.Gmail_API import send_email
from Util.Security import ts
from Settings.App_Settings import SECRETKEY, TRACKMODIFICATIONS
from Settings.DB_Settings import dbuser,dbpass,dbhost,dbname
from APIs import Wikipedia
from APIs.movies import movies
from APIs.spoiler import Spoiler
from flask_apscheduler import APScheduler
from itertools import count
import time

'''
Setup the app with all of its environment
'''
#region AppSetup
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

SPOILER = Spoiler()

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
#endregion


'''
Setup Classes Needed
'''
#region Classes
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

class SentSpoiler(db.Model,UserMixin):
    __tablename__ = 'SentSpoilers'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    from_user = db.Column(db.String(30), nullable=False)
    to_email = db.Column(db.String(30), nullable=False,unique=True)
    spoiler = db.Column(db.String(), nullable=False)
    date_sent = db.Column(db.String(50), nullable=False)

    def __init__(self, from_user, to_email, spoiler):
        self.from_user = from_user
        self.to_email = to_email
        self.spoiler = spoiler
        self.date_sent = date.today()

    def __repr__(self):
        return '<from: %r , to:%r , date: %r>' % self.from_user, self.to_email, self.date_sent




#endregion



'''
Setup Forms
'''
#region Forms
class RegistrationForm(FlaskForm):   
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    name = StringField('name',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=0, max=20)])

class LoginForm(FlaskForm):
    email = StringField('email',  validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=20)])

class PickAMovieForm(FlaskForm):
    movie_name = StringField('movie_name',  validators=[InputRequired(), Length(max=30)])

class BuildASpoiler(FlaskForm):
    movie_name = StringField('movie_name',  validators=[InputRequired(), Length(max=30)])
    victim_email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=30)])
    spoiler = TextAreaField('spoiler',  validators=[InputRequired()], id="spoiler")
#endregion

'''
User Management Authentication 
'''
#region User Managment

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
    
@app.route("/signup",methods=['GET','POST'])
def register_user():
    form = RegistrationForm()

    if request.method == 'GET':
        return render_template('user_management/signup.html', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            existing_email = User.query.filter_by(email=form.email.data).first()
            if existing_email is not None:
                return render_template('user_management/signup.html', form=form, error="Email taken")  # We should return a pop up error msg as well account taken
            else:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                newUser = User(name=form.name.data, email=form.email.data,password_hash=hashpass,number_interactions=1,date=date.today(),phone_number="")
                db.session.add(newUser)
                db.session.commit()
                login_user(newUser)
                return redirect(url_for('landing_page'))
        return render_template('user_management/signup.html', form=form, loggedin = current_user.is_authenticated) #We should return a pop up error msg as well bad input


@app.route("/login", methods=['GET', 'POST'])
def Login():
    form = LoginForm()

    if request.method == 'GET':

        if current_user.is_authenticated == True:
            return redirect(url_for('landing_page'))
        return render_template('user_management/login.html', form=form, loggedin = current_user.is_authenticated)

    elif request.method == 'POST':
        check_user = User.query.filter_by(email=form.email.data).first()
        if check_user:
            if check_password_hash(check_user.password_hash, form.password.data):
                login_user(check_user)
                session['email'] = form.email.data
                return redirect(url_for('landing_page'))
            return render_template('user_management/login.html', form=form, error="Incorrect password!", loggedin = current_user.is_authenticated)
        else:
            return render_template('user_management/login.html', form=form, error="Email doesn't exist!", loggedin = current_user.is_authenticated)

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    try:
        del session['access_token']
    except Exception:
        pass
    return redirect(url_for('Login'))

@app.route('/resetpassword', methods=["GET", "POST"])
def reset():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        subject = "Password reset requested"
        token = ts.dumps(user.email, salt='recover-key')
        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)
        html = render_template(
            'email/recover_password.html',
            recover_url=recover_url)

        send_email(user.email, subject, html)

        return redirect(url_for('landing_page'))

    return render_template('user_management/forgot_password.html', form=form)

@app.route('/resetpassword/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.password_hash = generate_password_hash(form.password.data, method='sha256')
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('Login'))

    return render_template('user_management/reset_password.html', form=form, token=token)

#endregion 


#region spoiler
@app.route("/getmovieinfo",methods=['GET'])     # Used for Autocomplete
def getmovieinfo():
    movie = request.args.get('term')
    movieC = movies()
    suggestions = movieC.getmoviesuggestions(movie)
    return jsonify(suggestions) 



@app.route("/pick-a-movie",methods=['GET','POST'])   
def pick_movie():
    form = PickAMovieForm()
    if request.method == 'GET':  
        return render_template('spoilers/pick_a_movie.html', form = form, loggedin = current_user.is_authenticated)

@app.route("/build-spoiler",methods=['GET','POST'])
def build_spoiler():
    dat = request.form
    try:
        name = dat.to_dict()['movie_name']
        if(name):
            spoiler = SPOILER.GenerateWikipediaSpoiler(name)
    except Exception:
        spoiler = None
    form = BuildASpoiler(spoiler=spoiler)
    return render_template('spoilers/build_a_spoiler.html', form = form, loggedin = current_user.is_authenticated, spoiler = spoiler)


counter = lambda c=count(): next(c)
@app.route("/scheduler-spoiler",methods=['GET','POST'])
def scheduler_spoiler():
    dat = request.form.to_dict()
    form = BuildASpoiler()
    newSpoiler = SentSpoiler(from_user = session['email'], to_email = dat['victim_email'], spoiler = dat['spoiler'])
    db.session.add(newSpoiler)
    db.session.commit()
    app.apscheduler.add_job(func=schedule_email, trigger='date', args=[dat['victim_email'],dat['spoiler']], id='j' + str(counter))
    return render_template('spoilers/build_a_spoiler.html', form = form, loggedin = current_user.is_authenticated)

def schedule_email(email,spoiler):
    send_email(email, "subject", spoiler)

#endregion


@app.route("/")
def landing_page():
    print(current_user.is_authenticated)
    return render_template('landing_page.html', loggedin = current_user.is_authenticated)


if __name__ == '__main__':
    app.run(debug=True)
