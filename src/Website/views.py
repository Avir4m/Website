from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from .models import User, Post, User, Comment, Like, Saved
from . import db

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=posts)

@views.route('/user/<username>/dashboard/', methods=['POST', 'GET'])
@login_required
def dashboard(username):
    if username == current_user.username:
        if request.method == 'POST':
            
            user = current_user
            
            email = request.form.get('email')
            username = request.form.get('userName')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            description = request.form.get('description')
            
            user_email = User.query.filter_by(email=email).first()
            user_name = User.query.filter_by(username=username).first()
            
            
            if user_email:
                if email == user.email:
                    pass
                else:
                    flash('This email is already in use.', category='error')
            if user_name:
                if username == user.username:
                    pass
                else:
                    flash('This username is already in use.', category='error')
            if email == user.email and username == user.username and first_name == user.first_name and last_name == user.last_name and description == user.description:
                flash('Can\'t update profile if nothing has been changed.', category='error')
            else:
                if first_name == '':
                    flash('First Name must be provided.', category='error')
                elif username == '':
                    flash('Username must be provided.', category='error')
                elif email == '':
                    flash('Email must be provided.', category='error')
                else:
                    user.email = email
                    user.username = username
                    user.first_name = first_name
                    user.last_name = last_name
                    user.description = description
                    db.session.commit()
                    flash('Profile has been updated.', category='success')
                
        return render_template('dashboard.html', user=current_user)
    
    else:
        return redirect(url_for('views.dashboard'), username=current_user.username)

@views.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = Post.query.filter_by(author=user.id).all()
    return render_template("user.html", user=current_user, posts=posts, username=user)

@views.route('/post/<username>/<url>/')
def post(username, url):
    post = Post.query.filter_by(url=url).first()
    posts = Post.query.filter_by(url=url).all()
    if not post:
        abort(404)
    else:
        return render_template('post.html', post=post, user=current_user, posts=posts)