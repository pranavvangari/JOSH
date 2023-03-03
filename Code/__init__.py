from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "profiles.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello world'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    from .views import views
    from .auth import auth

    

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #if we are not logged in go to login page
    login_manager.init_app(app) # telling the manager which app we're using
    
    

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #looks for primary key which is id. Tells flask what user we're looking for

    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    
    return app




'''
    def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app) 
        print('Created database')
'''
