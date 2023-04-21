
from cgi import print_environ_usage
from tabnanny import check
from unicodedata import category
from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response, Flask, abort
from importlib_metadata import re
import sqlite3
from flask_login import current_user, login_required, logout_user

#google login
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from pip._vendor import cachecontrol
import google.auth.transport.requests
from sre_parse import State
import os
import pathlib
import requests






views = Blueprint('views', __name__)



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "405828725907-bm4bdsfe6dpk7llrevcaev5louftvtc1.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri="http://127.0.0.1:5000/callback"  #and the redirect URI is the point where the user will end up after the authorization
)




def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row # goes through the database
    return connection

def get_classesDB_connection():
    classesConn = sqlite3.connect('CourseCatalog.db')
    classesConn.row_factory = sqlite3.Row
    return classesConn

def get_clubsDB_connection():
    clubsConnection = sqlite3.connect('RealDB.db')
    clubsConnection.row_factory = sqlite3.Row
    return clubsConnection
    

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

def update_grade(conn, task):

    """
    update Grade
    :param conn:
    :param task:
    :return: project id
    """
    
    sql = """ UPDATE Accounts SET Grade = ? WHERE id = ? """
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit() 

def login_is_required(function):  #a function to check if the user is authorized or not
    def trueWrapper(*args, **kwargs):
        if "google_id" not in session:  #authorization required
            flash('Please login with your google account', category='error')
            return render_template("loginPage.html")
            
        else:
            return function()

    return trueWrapper 



@views.route("/googleLogin")  #the page where the user can login
def googleLogin():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@views.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  #defing the results to show on the page
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table

    emailExists = 0
    for account in accounts:
        if account['Email'] == session["email"]:
            emailExists = 1

    if emailExists == 0:
        sql = """INSERT INTO Accounts(Name, Email) VALUES(?, ?)"""
        db_cursor = connection.cursor()
        
        account = (session["name"], session["email"])
        db_cursor.execute(sql, account)
        connection.commit()
        
    return redirect("/")  #the final page where the authorized users will end up

@views.route("/googleLogout")  #the logout page and function
def googleLogout():
    session.clear()
    return redirect("/loginPage")



@views.route('/loginPage')
def loginPage():
    
    return render_template("loginPage.html")


@views.route('/', methods=['GET', 'POST'], endpoint='home')
@login_is_required
def home():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    # write code here

    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
            acc = account

    
    

    



    return render_template("home.html", acc=acc)







@views.route('/findTutor', methods=['GET', 'POST'], endpoint='findTutor')
@login_is_required
def findTutor():
    
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    connection.close()
    

    return render_template("findTutor.html", accounts=accounts)

    
 
@views.route('/myProfile', methods=['GET', 'POST'], endpoint='myProfile')
@login_is_required
def myProfile():
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    bio = request.form.get('bio')
    grade = request.form.get('grade')


    
    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
            acc = account
    
    
    tempProfilePicture = acc['ProfilePicture']
    s2 = tempProfilePicture
    s1 = 'pictures/'


    profilePicture = "%s %s" % (s1, s2)


    
    if request.method == 'POST':

        #code that updates bio
        print("this is bio")
        print(bio)
        if (bio == ""):
            print("dont print")
            
            
        else: 
            update_bio(connection, (bio, acc['ID']))
            flash('Bio updated successfully!', category='success')


    
    
    tutorCheckboxValueDB = acc['TutorValue']
    grade = acc['Grade']
    
    
    connection.close()

    return render_template("myProfile.html", acc=acc, profilePicture=profilePicture, tutorCheckboxValueDB=tutorCheckboxValueDB, grade=grade) 

@views.route('/aboutUs')
def aboutUs():
    
    return render_template("aboutUs.html")





@views.route('<Info>')
# url_for run through html in files: classeTable.html(course_id) and findTutor.html(email)
def renderInfo(Info):
    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table

    dbConn = get_classesDB_connection()
    lstCourse = dbConn.execute('''select * from Catalog''').fetchall()
    
    clubsConnection = get_clubsDB_connection()
    clubs = clubsConnection.execute('SELECT * from clubs LEFT JOIN weekdays on clubs.name = weekdays.name').fetchall()

    methodNumber = 1

    for letter in Info:
        if letter == '@':
            methodNumber = 2
        

    if '--' in Info:
        methodNumber = 3

    if methodNumber == 1:
        return render_template('classTemplate.html', classes=Info, lstCourse=lstCourse)
    elif methodNumber == 2:
        acc = 1
        for account in accounts:
            if Info == account['Email']:
                acc = account

        tempProfilePicture = acc['ProfilePicture']
        s2 = tempProfilePicture
        s1 = 'pictures/'
        tutorProfilePicture = "%s %s" % (s1, s2)
        return render_template('tutor.html', accounts=accounts, email=Info, tutorProfilePicture=tutorProfilePicture)
    elif methodNumber == 3:
        return render_template("clubTemplate.html", clubs=clubs, Name=Info)





@views.route('/profilePicChange', methods=['GET', 'POST'], endpoint='profilePicChange') 
@login_is_required
def profilePicChange(): 


    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall()
    c = connection.cursor()
    
    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
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
        c.execute(sql, (filename, acc['ID']))

        #Note: make it so that WHERE statement checks for email, not id; it will be faster
        
        connection.commit()
    
    
    
    connection.close()
   
    #file.save("c:/Users/pranav.vangari/Desktop/addMP/Code/static/pictures/hi.jpg")
    #os.getcwd()
        
    
    return render_template('profilePicChange.html' , profilePic=profilePic )


@views.route('/classes', endpoint='classes')
@login_is_required

def classes():
    classesConn = get_classesDB_connection()
    classes = classesConn.execute('SELECT * FROM Catalog').fetchall()




    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table

    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
            acc = account

    classesFromDB = acc['SubjectsTaught']


    return render_template("classes.html", classes=classes, acc=acc, classesFromDB=classesFromDB)



@views.route('/temp', methods=['Get', 'POST'], endpoint='temp')
@login_is_required
def temp():

    

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table

    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
            acc = account

    classesFromDB = acc['SubjectsTaught']
    classesSplit = -1
    


    return render_template("temp.html")


@views.route('/send_tutorValue', methods=['POST'])
# method run through js
def send_value():
    value_received = request.json['tutorValue']

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    
    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
            acc = account

    update_tutorValue(connection, (value_received, acc['ID']))
    

    print("js works") 
    print(value_received)

    


    return render_template("home.html")


@views.route('/checkedClasses', methods=['POST'])
# function run through js
def classesChecked():

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    tempVar = "works"
    value_received = request.json['classesNames']  

    print(value_received)

    if len(value_received) > 0:
        classesString = value_received[0]
    else:
        classesString = None
    
    for x in value_received:
    
        if x != classesString:
            classesString = classesString + ", " + x


    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
            acc = account
        

    update_subjectsTaught(connection, (classesString, acc['ID']))


    
     
    
    return render_template("home.html")


@views.route('/send_grade', methods=['POST'])
# function run in js 
def send_grade():
    gradeRecieved = request.json['grade']

    connection = get_db_connection()
    accounts = connection.execute('SELECT * FROM Accounts').fetchall() # selects everything from Accounts table
    
    

    acc = 1
    for account in accounts:
        if account['Email'] == session['email']:
            acc = account

    
    update_grade(connection, (gradeRecieved, acc['ID']))
    

    
    return render_template("home.html")



#
#
#
# Classes Aspect - From Alexander and Michael

@views.route('/classesTable', endpoint='classesTable')
@login_is_required
def classesTable():
    classesConn = get_classesDB_connection()
    lstCourse = classesConn.execute('''select * from Catalog''').fetchall()
    #code to filter the subject list
    cursor = classesConn.cursor()
    cursor.execute("SELECT subject FROM catalog")
    rows = cursor.fetchall()
    data = [row[0] for row in rows]
    data = list(set(data))
    classesConn.close()
    return render_template("classesTable.html", lstCourse=lstCourse, data=data)

@views.route('/grading', endpoint='grading')
@login_is_required
def grading():
    return render_template("grading.html")

@views.route('/blended', endpoint='blended')
@login_is_required
def blended():
    return render_template("blended.html")

#
#
#
#
# Clubs Aspect - Yehan and Ansel's code

@views.route('/clubsTable', endpoint='clubsTable')
@login_is_required
def clubsTable():
    clubsConnection = get_clubsDB_connection()
    clubs = clubsConnection.execute('SELECT * from clubs LEFT JOIN weekdays on clubs.name = weekdays.name').fetchall()

    return render_template("clubsTable.html", clubs=clubs)


