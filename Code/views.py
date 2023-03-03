from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from importlib_metadata import re
import sqlite3
from .models import User
from . import db
from flask_login import current_user, login_required, logout_user
import os



views = Blueprint('views', __name__)


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row # goes through the database
    return connection
    

def update_bio(conn, task):
    
    """
    update Bio
    :param conn:
    :param task:
    :return: project id
    """
    
    sql = """ UPDATE Accounts SET Bio = ? WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    # write code here

    acc = 1
    for account in accounts:
        if current_user.id == account['ID']:
            acc = account

    return render_template("home.html", accounts=accounts, acc=acc)



@views.route('/findTutor', methods=['GET', 'POST'])
def findTutor():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    connection.close()
    

    return render_template("findTutor.html", accounts=accounts)

    

@views.route('/myProfile', methods=['GET', 'POST'])
def myProfile():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    bio = request.form.get('bio')

    acc = 1
    for account in accounts:
        if current_user.id == account['ID']:
            acc = account

    tempProfilePicture = acc['ProfilePicture']
    s2 = tempProfilePicture
    s1 = 'pictures/'


    profilePicture = "%s %s" % (s1, s2)


    if request.method == 'POST':

        update_bio(connection, (bio, current_user.id))
        flash('Bio updated successfully!', category='success')
    
    connection.close()
    

    return render_template("myProfile.html", accounts=accounts, acc=acc, profilePicture=profilePicture)


@views.route('<Email>')
def renderInfo(Email):
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table

    acc = 1
    for account in accounts:
        if Email == account['Email']:
            acc = account

    tempProfilePicture = acc['ProfilePicture']
    s2 = tempProfilePicture
    s1 = 'pictures/'
    tutorProfilePicture = "%s %s" % (s1, s2)

    return render_template('tutor.html', accounts=accounts, email=Email, tutorProfilePicture=tutorProfilePicture)




@views.route('/profilePicChange', methods=['GET', 'POST']) 
def profilePicChange(): 
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall()
    c = connection.cursor()

    acc = 1
    for account in accounts:
        if current_user.id == account['ID']:
            acc = account

    profilePic = acc['ProfilePicture']
    
    if request.method == 'POST': 

        file = request.files['image']
        filename = file.filename
        s1 = filename
        s2 = 'c:/Users/pranav.vangari/Desktop/addMP/Code/static/pictures/'
        s3 = "%s %s" % (s2, s1)

        file.save(s3)

        sql = ('UPDATE Accounts SET ProfilePicture = ? WHERE id = ?')
        c.execute(sql, (filename, current_user.id))
        
        connection.commit()
    
    connection.close()
   
    #file.save("c:/Users/pranav.vangari/Desktop/addMP/Code/static/pictures/hi.jpg")
    #os.getcwd()
        
    
    return render_template('profilePicChange.html', profilePic=profilePic )
        
