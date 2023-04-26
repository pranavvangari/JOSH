<<<<<<< HEAD
from flask import Flask, request, flash, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
=======
from flask import Flask
>>>>>>> 77df6ec0d0e5b0209bc4fe5e4cd3d44ef214a308


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hello world'

    

    from .views import views

    

    app.register_blueprint(views, url_prefix='/')
    
        
    
    return app



