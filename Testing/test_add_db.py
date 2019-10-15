from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from flask_wtf.csrf import CSRFProtect
from Settings.DB_Settings import dbuser,dbpass,dbhost
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.config['SECRET_KEY'] = 'VeryVerySecretKeyandWhatNot1203491324'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(dbuser,dbpass,dbhost,dbuser)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Classes
class User(db.Model):
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



me = User('test3@testing.com',generate_password_hash('ajsfdkhakjsfhak', method='sha256'), 'test mctesterson3',date.today(),'35265086432',1 )

db.session.add(me)
db.session.commit()

peter = User.query.filter_by(email='test3@testing.com').all()
print(peter)