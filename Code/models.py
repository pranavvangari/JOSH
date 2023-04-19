'''
from . import db 
from flask_login import UserMixin

class User(db.Model, UserMixin):
    #using UserMixin because we use flask_login  
    id = db.Column(db.Integer, primary_key=True)  
    email = db.Column(db.String(150), unique=True) #unique=True makes it so that every email has to be different, no repeats. String(150) means a max of 150 characters
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    bio = db.Column(db.String(2000))

'''
