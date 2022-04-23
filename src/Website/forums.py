from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
import os

from .models import Forum
from .func import create_url, allowed_file, unique_filename
from . import db

forums = Blueprint('forums', __name__)

@forums.route('/create-forum', methods=['POST', 'GET'])
@login_required
def create_forum():
    if request.method == 'POST':
        name = request.form.get('forumName')
        description = request.form.get('forumDescription')
        
        forum = Forum.query.filter_by(name=name).first()
        
        file = request.files['file']
        
        if forum:
            flash('forum name already exists, please change forum name.', category='error')
        elif len(name) <= 2:
            flash('forum name must be at least 2 characters', category='error')
        else:
            if file and allowed_file(file.filename):
                filename, ext = secure_filename(file.filename).split('.')
                filename = unique_filename(filename, Forum) + '.' + ext
                file.save(os.path.join(os.getcwd(), 'src/website/static/images/upload_folder/forums/', filename))
                forum = Forum(name=name, description=description, creator=current_user.id, url=create_url(Forum), picture=filename)
            else:
                forum = Forum(name=name, description=description, creator=current_user.id, url=create_url(Forum))
            db.session.add(forum)
            db.session.commit()
            flash('forum created successfully!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('create_forum.html', user=current_user)
    
@forums.route('/delete-forum/<forum_id>')
@login_required
def delete_forum(forum_id):
    forum = Forum.query.filter_by(id=forum_id).first()
    
    if not forum:
        flash('forum does not exists.', category='error')
    elif current_user.id != forum.creator and current_user.permissions <= 1:
        flash('you do not have permission to delete this forum.', category='error')
    else:
        db.session.delete(forum)
        db.session.commit()
        flash('forum has been deleted.', category='success')
        
    return redirect(url_for('views.home'))

@forums.route('/edit-forum/<forum_id>', methods=['POST', 'GET'])
@login_required
def edit_forum(forum_id):
    forum = Forum.query.filter_by(id=forum_id).first()
    
    if not forum:
        abort(404)
    if request.method == 'POST':
        if not forum:
            flash('forum does not exists.', category='error')
        elif current_user.id != forum.creator:
            flash('you do not have permission to delete this forum.', category='error')
        else:
            new_name = request.form.get('newName')
            new_description = request.form.get('newDescription')
            
            file = request.files['file']
        
            if file and allowed_file(file.filename):
                filename, ext = secure_filename(file.filename).split('.')
                new_filename = unique_filename(filename, Forum) + '.' + ext
                file.save(os.path.join(os.getcwd(), 'src/website/static/images/upload_folder/forums/', new_filename))
                forum.picture = new_filename
                db.session.commit()
            
            if len(new_name) <= 2:
                flash('forum name must be at least 2 characters.', category='error')
            else:
                forum.name = new_name
                forum.description = new_description
                forum.edited = True
                db.session.commit()
                flash('forum name has been updated.', category='success')
                return redirect(url_for('views.forum', url=forum.url))
                
    
    return render_template('edit_forum.html', user=current_user, forum=forum)