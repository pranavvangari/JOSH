from flask import Flask, request, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello world'

    

    from .views import views

    

    app.register_blueprint(views, url_prefix='/')
    
        
    
    return app



