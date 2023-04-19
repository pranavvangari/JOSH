from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask
from flask_login import login_user, login_required, logout_user, current_user, LoginManager, UserMixin
import sqlite3

from Code.views import temp
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message



auth = Blueprint('auth', __name__)

# configs for flask_mail
#download pip install flask_mail==0.9.0








def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row # goes through the database
    return connection

@auth.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() #filter_by(email=email) looks at user with the email and .first is the first time the email occurs

        if user:
            if check_password_hash(user.password, password): #uses second password and compares it to the first password
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password, try again', category='error')
        else:
            flash('email does not exist', category='error')


    return render_template("login.html", user=current_user )
    
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall()
    sql = """INSERT INTO Accounts(firstName, lastName, Email, Password, Grade) VALUES(?, ?, ?, ?, ?)"""
    db_cursor = connection.cursor()

    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        grade = request.form.get('grade')
        
        
        
        if "@student158.org" not in email:
            flash('Email must be Huntley student email', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character!', category='error')
        elif len(last_name) < 2:
            flash('First Name must be greater than 1 character!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(password1) < 3:
            flash('Password must be at least 3 characters!', category='error')
        elif grade == 'temp':
            flash('Choose a grade', category='error')
        else:
            account = (first_name, last_name, email, password1, grade)
            db_cursor.execute(sql, account)
            connection.commit()
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(user, remember=True)
            flash('Account created successfully', category='success')
            user = User.query.filter_by(email=email).first()
            login_user(user, remember=True)
            return redirect(url_for('views.home')) #changes screen after account was created successfully to home page
        

        connection.close()

    return render_template("signup.html")