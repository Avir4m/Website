from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user

from .models import User, Post, Comment, Like, Saved, Forum, Report

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
def dashboard():
    per = current_user.permissions # Permissions
    if per >= 1:
        users = User.query.filter_by().all()
        posts = Post.query.filter_by().all()
        comments = Comment.query.filter_by().all()
        likes = Like.query.filter_by().all()
        saves = Saved.query.filter_by().all()
        forums = Forum.query.filter_by().all()
        reports = Report.query.filter_by().all()
        
        post_reports = Report.query.filter_by(forum_id=None).all()
        forums_reports = Report.query.filter_by(post_id=None).all()
        
        return render_template('admin/dashboard.html', user=current_user,
                               users=users, posts=posts, comments=comments, likes=likes, saves=saves, forums=forums, # Models
                               reports=reports,forums_reports=forums_reports, post_reports=post_reports) # Reports
    else:
        abort(403)

@admin.route('/users/')
@login_required
def users():
    per = current_user.permissions # Permissions
    if per >= 1:
        users = User.query.filter_by().all()
        return render_template('admin/models/users.html', user=current_user, users=users)
    else:
        abort(403)
        
@admin.route('/posts/')
@login_required
def posts():
    per = current_user.permissions # Permissions
    if per >= 1:
        posts = Post.query.filter_by().all()
        return render_template('admin/models/posts.html', user=current_user, posts=posts)
    else:
        abort(403)
        
@admin.route('/forums/')
@login_required
def forums():
    per = current_user.permissions # Permissions
    if per >= 1:
        forumss = Forum.query.filter_by().all()
        return render_template('admin/models/forumss.html', user=current_user, forumss=forumss)
    else:
        abort(403)

@admin.route('/comments/')
@login_required
def comments():
    per = current_user.permissions # Permissions
    if per >= 1:
        comments = Comment.query.filter_by().all()
        return render_template('admin/models/comments.html', user=current_user, comments=comments)
    else:
        abort(403)
        
@admin.route('/likes/')
@login_required
def likes():
    per = current_user.permissions # Permissions
    if per >= 1:
        likes = Like.query.filter_by().all()
        return render_template('admin/models/likes.html', user=current_user, likes=likes)
    else:
        abort(403)
        
@admin.route('/saves/')
@login_required
def saves():
    per = current_user.permissions # Permissions
    if per >= 1:
        saves = Saved.query.filter_by().all()
        return render_template('admin/models/saves.html', user=current_user, saves=saves)
    else:
        abort(403)
        
@admin.route('/reports/')
@login_required
def reports():
    per = current_user.permissions # Permissions
    if per >= 1:
        reports = Report.query.filter_by().all()
        return render_template('admin/reports/reports.html', user=current_user, reports=reports)
    else:
        abort(403)
        
@admin.route('/reports/posts/')
@login_required
def reports_posts():
    per = current_user.permissions # Permissions
    if per >= 1:
        reports = Report.query.filter_by(forums_id=None).all()
        return render_template('admin/reports/posts.html', user=current_user, reports=reports)
    else:
        abort(403)
        
@admin.route('/reports/forums/')
@login_required
def reports_forums():
    per = current_user.permissions # Permissions
    if per >= 1:
        reports = Report.query.filter_by(post_id=None).all()
        return render_template('admin/reports/forumss.html', user=current_user, reports=reports)
    else:
        abort(403)