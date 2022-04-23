from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
import os

from .models import Post, Like, Saved, Forum
from .func import create_url, unique_filename, allowed_file
from . import db

posts = Blueprint('posts', __name__)

@posts.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    forums = Forum.query.filter_by().all()
    
    if request.method == 'POST':
        title = request.form.get('post-title')
        text = request.form.get('post-text')
        forumName = request.form.get('forum')
        
        file = request.files['file']
        
        forum = Forum.query.filter_by(name=forumName).first()
        
        if not title:
            flash('Post title cannot be empty', category='error')
        elif len(title) >= 150:
            flash('Post title is too long.', category='error')
        elif not text:
            flash('Post text cannot be empty', category='error')
        elif not forum and forumName != '':
            flash('Forum does not exist.', category='error')
        else:
            if forumName == '':
                forum_id=None
            else:
                forum_id = forum.id
            if file and allowed_file(file.filename):
                filename, ext = secure_filename(file.filename).split('.')
                filename = unique_filename(filename, Forum) + '.' + ext
                file.save(os.path.join(os.getcwd(), 'src/website/static/images/upload_folder/posts/', filename))
            else:
                filename = None
                
            post = Post(title=title ,text=text, author=current_user.id, url=create_url(Post), forum_id=forum_id, picture=filename)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template('create_post.html', user=current_user, forums=forums)


@posts.route('/delete-post/<post_id>/')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        flash('Post does not exists.', category='error')
    elif current_user.id != post.author and current_user.permissions <= 1:
        flash('you do not have permission to delete this post.', category='error')
    else:
        if post.comments:
            for comment in post.comments:
                db.session.delete(comment)
                db.session.commit()
        if post.likes:
            for like in post.likes:
                db.session.delete(like)
                db.session.commit()
        if post.saves:
            for saved in post.saves:
                db.session.delete(saved)
                db.session.commit()
        if post.reports:
            for report in post.reports:
                db.session.delete(report)
                db.session.commit()
                
        db.session.delete(post)
        db.session.commit()
        flash('Post has been deleted.', category='success')
        
    return redirect(url_for('views.home'))


@posts.route('/edit-post/<post_id>/', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        abort(404)
    if request.method == 'POST':
        if not post:
            flash('This post does not exist.', category='error')
        elif post.author != current_user.id:
            flash('You are not allowed to edit this post.', category='error')
        else:
            new_post_title = request.form.get('newPostTitle')
            new_post_text = request.form.get('newPostText')
            
            if new_post_title == '':
                flash('Post title cannot be empty.', category='error')
            elif new_post_text == '':
                flash('Post text cannot be empty.', category='error')
            else:
                post.title = new_post_title
                post.text = new_post_text
                post.edited = True
                db.session.commit()
                flash('Post has been updated.', category='success')
                return redirect(url_for('views.home'))
            
            return render_template('edit_post.html', user=current_user, post=post)
    else:
        return render_template('edit_post.html', user=current_user, post=post)


@posts.route('/like-post/<post_id>/', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        
    return jsonify({'likes': len(post.likes), 'liked': current_user.id in map(lambda x: x.author, post.likes)})

@posts.route('/post-status/<post_id>')
@login_required
def post_status(post_id):
    post = Post.query.filter_by(id=post_id).first()
    status = post.private
    if not post:
        flash('This post does not exist.', category='error')
    elif post.author != current_user.id:
        abort(403)
    elif status:
        post.private = False
        db.session.commit()
    else:
        post.private = True
        db.session.commit()
        
    return redirect(url_for('views.home'))

@posts.route('/save-post/<post_id>/', methods=['POST'])
@login_required
def save_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    saved = Saved.query.filter_by(author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif saved:
        db.session.delete(saved)
        db.session.commit()
    else:
        saved = Saved(post_id=post_id, author=current_user.id)
        db.session.add(saved)
        db.session.commit()
        
    return jsonify({'saved': current_user.id in map(lambda x: x.author, post.saves)})
