from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user


from .models import Post, Report, Forum
from .func import create_url
from . import db

reports = Blueprint('reports', __name__)

@reports.route('/create-report/post/<url>/', methods=['POST', 'GET'])
@login_required
def report_post(url):
    post = Post.query.filter_by(url=url).first()
    if not post:
        abort(404)
        
    if request.method == 'POST':
        description = request.form.get('description')
        reason = request.form.get('reason')
        
        report = Report(description=description, reason=reason, author=current_user.id, post_id=post.id)
        db.session.add(report)
        db.session.commit()
        flash('Post has been reported!', category='success')
        return redirect(url_for('views.post', url=url))
        
    return render_template('reports/post.html', user=current_user, post=post)

@reports.route('/create-report/forum/<url>/', methods=['POST', 'GET'])
@login_required
def report_forum(url):
    forum = Forum.query.filter_by(url=url).first()
    if not forum:
        abort(404)
    
    if request.method == 'POST':
        description = request.form.get('description')
        reason = request.form.get('reason')
        
        report = Report(description=description, reason=reason, author=current_user.id, forum_id=forum.id)
        db.session.add(report)
        db.session.commit()
        flash('Forum has been reported!', category='success')
        return redirect(url_for('views.forum', url=url))
    
    return render_template('reports/forum.html', user=current_user, forum=forum)