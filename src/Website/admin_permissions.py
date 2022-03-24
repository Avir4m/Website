from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from .models import User, Post, Comment

admin_permissions = Blueprint('admin', __name__)

@admin_permissions.route('/')
@login_required
def dashboard():
    per = current_user.permissions # Permissions
    if per >= 1:
        users = User.query.filter_by().all()
        posts = Post.query.filter_by().all()
        comments = Comment.query.filter_by().all()
        return render_template('admin/dashboard.html', user=current_user, users=users, posts=posts, comments=comments)
    else:
        abort(403)

@admin_permissions.route('/users/')
@login_required
def users():
    per = current_user.permissions # Permissions
    if per >= 1:
        users = User.query.filter_by().all()
        return render_template('admin/users.html', user=current_user, users=users)
    else:
        abort(403)
        
@admin_permissions.route('/posts/')
@login_required
def posts():
    per = current_user.permissions # Permissions
    if per >= 1:
        posts = Post.query.filter_by().all()
        return render_template('admin/posts.html', user=current_user, posts=posts)
    else:
        abort(403)

@admin_permissions.route('/comments/')
@login_required
def comments():
    per = current_user.permissions # Permissions
    if per >= 1:
        comments = Comment.query.filter_by().all()
        return render_template('admin/comments.html', user=current_user, comments=comments)
    else:
        abort(403)