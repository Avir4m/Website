from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user

import uuid

from .models import Post, Like, Saved
from . import db

posts = Blueprint('posts', __name__)

@posts.route('/create-post', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form.get('post-title')
        text = request.form.get('post-text')
        if not title:
            flash('Post title cannot be empty', category='error')
        elif len(title) >= 150:
            flash('Post title is too long.', category='error')
        elif not text:
            flash('Post text cannot be empty', category='error')
        else:
            def create_url():
                url = uuid.uuid4().hex
                post = Post.query.filter_by(url=url).first()
                if post:
                    create_url()
                else:
                    return url
                
            post = Post(title=title ,text=text, author=current_user.id, url=create_url())
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template('create_post.html', user=current_user)


@posts.route('/delete-post/<post_id>/')
@login_required
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    
    if not post:
        flash('Post does not exists.', category='error')
    elif current_user.id != post.author:
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
        db.session.delete(post)
        db.session.commit()
        flash('Post delete.', category='success')
        
    return redirect(url_for('views.home'))


@posts.route('/edit-post/<post_id>/', methods=['POST', 'GET'])
@login_required
def edit_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
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
        
    return redirect(url_for('views.post', url=post.url, username=post.user.username))

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
