from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

with open("files/SECRET_KEY.txt", "r") as f:
    SECRET_KEY = f.read()
    f.close()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .ctrl import ctrl
    from .errors import errors
    from .admin_permissions import admin_permissions
     
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(ctrl, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')
    app.register_blueprint(admin_permissions, url_prefix='/')
    
    from .models import User, Post, Comment, Like, Saved
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if path.exists('Src/Website/' + DB_NAME):
        print(' * Loaded database')
    else:
        db.create_all(app=app)
        print(' * Created database')