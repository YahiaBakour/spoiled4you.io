import sys
import unittest
from main import *

matrix_plot = b'Computer programmer Thomas Anderson, known in the hacking scene by his alias "Neo", feels something is wrong with the world and is puzzled by repeated online encounters with the phrase "the Matrix." Trinity contacts him and tells him a man named Morpheus has the answers he seeks. The Agents, led by Agent Smith, apprehend Neo and threaten him into helping them capture the "terrorist" Morpheus. Undeterred, Neo later meets Morpheus, who offers him a choice between two pills; red to show him the truth about the Matrix, and blue to return him to his former life. After Neo swallows the red pill, his reality disintegrates, and he awakens in a liquid-filled pod among countless others attached to an elaborate electrical system. He is retrieved and brought aboard Morpheus\' hovercraft, the Nebuchadnezzar.'

db = SQLAlchemy(app)

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



 


class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client() 
        self.assertEqual(app.debug, False)
        


    def register(self, name, email, password, confirm):
        return self.app.post(
            '/signup',
            data=dict(name=name,email=email, password=password, confirmPassword=confirm),
            follow_redirects=True
        )
    
    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def buildspoiler(self, movie_name):
        return self.app.post(
            '/build-spoiler',
            data=dict(movie_name=movie_name),
            follow_redirects=True
        )

    def logout(self):
        return self.app.get(
            '/logout',
            follow_redirects=True
        )

###############
#### tests ####
###############
 
    def test_landing_page(self):            #Not Logged In, Should go straight to Login
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Made by Yahia Bakour',response.data)

    def test_login_page(self):           #Not Logged In, Should go straight to page
        response = self.app.get('/login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):           #Not Logged In, Should go straight to page
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_about_us_page(self):
        response = self.app.get('/about-us', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'How it started',response.data)


    def test_valid_user_registration(self):
        response = self.register('meowmeow','meowmeow@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congrats on signing up', response.data)
        User.query.filter_by(email='meowmeow@gmail.com').delete()
        db.session.commit()
        
    def test_taken_user_registration(self):
        self.register('meowmeow','meowmeow@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        response = self.register('meowmeow','meowmeow@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email taken', response.data)
        User.query.filter_by(email='meowmeow@gmail.com').delete()
        db.session.commit()
        
    def test_user_login(self):
        response = self.login('test3@testing.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/logout', response.data)

    def test_user_invalid_email_login(self):
        response = self.login('meowmeow2@gmail.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email doesn", response.data)


    def test_user_invalid_password_login(self):
        response = self.login('test3@testing.com', 'FlaskIsAwesome2')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incorrect password', response.data)

    def test_get_movie_page(self):
        self.login('test3@testing.com', 'FlaskIsAwesome')
        response = self.app.get('/pick-a-movie',follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Create your spoiler',response.data)


    def test_the_matrix_spoiler(self):
        self.login('test3@testing.com', 'FlaskIsAwesome')
        response = self.buildspoiler("The Matrix")
        self.assertEqual(response.status_code,200)
        self.assertIn(matrix_plot,response.data)

if __name__ == '__main__':
    unittest.main()