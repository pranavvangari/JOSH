
from cgi import print_environ_usage
from tabnanny import check
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from importlib_metadata import re
import sqlite3
from .models import User
from . import db
from flask_login import current_user, login_required, logout_user
from bs4 import BeautifulSoup
import requests

#checkbox imports
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox
import sys
import tkinter as tk



views = Blueprint('views', __name__)


def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row # goes through the database
    return connection

def get_classesDB_connection():
    classesConn = sqlite3.connect('CourseCatalog.db')
    classesConn.row_factory = sqlite3.Row
    return classesConn
    

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

def update_tutorValue(conn, task):
    
    """
    update TutorValue
    :param conn:
    :param task:
    :return: project id
    """
    
    sql = """ UPDATE Accounts SET TutorValue = ? WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def update_subjectsTaught(conn, task):

    """
    update SubjectsTaught
    :param conn:
    :param task:
    :return: project id
    """
    
    sql = """ UPDATE Accounts SET SubjectsTaught = ? WHERE id = ? """
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
@login_required
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

    id = current_user.id


    checkbox  = request.form.get('checkboxTemp')
    print("newcheckbox")
    print(checkbox)

    if request.method == 'POST':

        #code that updates bio
        print("this is bio")
        print(bio)
        if (bio == ""):
            print("dont print")
            
            
        else: 
            update_bio(connection, (bio, current_user.id))
            flash('Bio updated successfully!', category='success')

    
    connection.close()
    

    return render_template("myProfile.html", accounts=accounts, acc=acc, profilePicture=profilePicture)

@views.route('/aboutUs')
def aboutUs():
    
    return render_template("aboutUs.html")


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


@views.route('/classes')
def classes():
    classesConn = get_classesDB_connection()
    classes = classesConn.execute('SELECT * FROM Catalog').fetchall()

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table

    acc = 1
    for account in accounts:
        if current_user.id == account['ID']:
            acc = account



    return render_template("classes.html", classes=classes, acc=acc)


@views.route('/temp', methods=['Get', 'POST', 'MYMETHOD'])
def temp():

    if request.method == 'POST':
        checkbox1 = request.form.get('checkbox1')
        checkbox2 = request.form.get('checkbox2')
        checkbox3 = request.form.get('checkbox3')

        # Store the checkbox values in a cookie
        response = make_response('Checkbox values stored!')
        response.set_cookie('checkbox1', checkbox1)
        response.set_cookie('checkbox2', checkbox2)
        response.set_cookie('checkbox3', checkbox3)

    checkbox1 = request.cookies.get('checkbox1', '')
    checkbox2 = request.cookies.get('checkbox2', '')
    checkbox3 = request.cookies.get('checkbox3', '')

    return render_template("temp.html", checkbox1=checkbox1, checkbox2=checkbox2, checkbox3=checkbox3)


    


    return render_template("temp.html")

@views.route('/send_tutorValue', methods=['POST'])
def send_value():
    value_received = request.json['tutorValue']

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    
    

    update_tutorValue(connection, (value_received, current_user.id))
    

    print("js works") 
    print(value_received)
    return render_template("home.html")

@views.route('/checkedClasses', methods=['POST'])
def classesChecked():

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    tempVar = "works"
    value_received = request.json['classesNumber']

    classesString = value_received[0]
    for x in value_received:
        print("we are")
        print(x)
        if x != classesString:
            classesString = classesString + ", " + x

    print(classesString)

    update_subjectsTaught(connection, (classesString, current_user.id))


    

    


    print(value_received)



    #update_subjectsTaught(connection, (tempVar, current_user.id))


     
    return render_template("home.html")
        
