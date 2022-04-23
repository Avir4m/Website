from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
with open("files/SECRET_KEY.txt", "r") as f:
    SECRET_KEY = f.read()
    f.close()

DB_NAME = "database.db"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    from .posts import posts
    from .comments import comments
    from .forums import forums
    from .reports import reports
    from .errors import errors
    from .admin import admin
     
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(posts, url_prefix='/')
    app.register_blueprint(comments, url_prefix='/')
    app.register_blueprint(forums, url_prefix='/')
    app.register_blueprint(reports, url_prefix='/')
    app.register_blueprint(errors, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    
    from .models import User
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('Src/Website/' + DB_NAME):
        print(' * Created database')
        db.create_all(app=app)
    else:
        print(' * Loaded database')