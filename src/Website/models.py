from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150), nullable=True)
    description = db.Column(db.String(200), nullable=False, default="")
    picture = db.Column(db.String(), default="default_profile_pic.jpg")
    date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    permissions = db.Column(db.Integer(), default=0)
    verified = db.Column(db.Boolean(), default=False)
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comment', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)
    saves = db.relationship('Saved', backref='user', passive_deletes=True)
    forums = db.relationship('Forum', backref='user', passive_deletes=True)
    reports = db.relationship('Report', backref='user', passive_deletes=True)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    text = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String, default=None)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    url = db.Column(db.String(150), nullable=False, unique=True)
    edited = db.Column(db.Boolean(), default=False)
    private = db.Column(db.Boolean(), default=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)
    saves = db.relationship('Saved', backref='post', passive_deletes=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id', ondelete="CASCADE"), nullable=True)
    reports =  db.relationship('Report', backref='post', passive_deletes=True)
    
class Saved(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    edited = db.Column(db.Boolean(), default=False)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    
class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=True)
    picture = db.Column(db.String(), default=None)
    edited = db.Column(db.Boolean(), default=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    url = db.Column(db.String(150), nullable=False, unique=True)
    posts = db.relationship('Post', backref='forum', passive_deletes=True)
    reports =  db.relationship('Report', backref='forum', passive_deletes=True)
    
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=True)
    forum_id = db.Column(db.Integer, db.ForeignKey('forum.id', ondelete="CASCADE"), nullable=True)