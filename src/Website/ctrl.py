from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from .models import User, Post, User, Comment, Like
from . import db

ctrl = Blueprint('ctrl', __name__)


@ctrl.route('/create-post', methods=['POST', 'GET'])
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
            post = Post(title=title ,text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))
            
    return render_template('create_post.html', user=current_user)

@ctrl.route('/delete-post/<id>')
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    
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

@ctrl.route('/delete-user/<id>', methods=['POST', 'GET'])
@login_required
def delete_user(id):
    per = current_user.permissions # Permissions
    if per >= 1:
        user = User.query.filter_by(id=id).first()
        posts = Post.query.filter_by(author=user.id).all()
        comments = Comment.query.filter_by(author=user.id).all()
        likes = Like.query.filter_by(author=user.id).all()
        if posts or comments or likes:
            for post in posts:
                db.session.delete(post)
                db.session.commit()
            for comment in comments:
                db.session.delete(comment)
                db.session.commit()
            for like in likes:
                db.session.delete(like)
                db.session.commit()
            db.session.delete(user)
            db.session.commit()
        else:
            db.session.delete(user)
            db.session.commit()
        flash('User has been deleted!', category='success')
        return redirect(url_for('admin.admin'))
    elif current_user.id == id:
        db.session.delete(current_user)
        db.session.commit()
        flash('User has been deleted!', category='success')
        return redirect(url_for('auth.sign_up'))
    else:
        flash('You dont have permission to delete this user!', category='error')
        
    return redirect(url_for('admin.admin'))

@ctrl.route('/create-comment/<post_id>', methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id).first()
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))

@ctrl.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))

@ctrl.route('like-post/<post_id>')
@login_required
def like_post(post_id):
    post = Post.query.filter_by(id=post_id)
    like = Like.query.filter_by(author=current_user.id).first()
    if not post:
        flash('This post does not exist.', category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
        
    return redirect(url_for('views.home'))

@ctrl.route('edit-post/<post_id>', methods=['POST', 'GET'])
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
            
            post.title = new_post_title
            post.text = new_post_text
            post.edited = True
            db.session.commit()
            flash('Post has been updated.', category='success')
            
            return redirect(url_for('views.home'))
    else:
        return render_template('edit_post.html', user=current_user, post=post)
    
@ctrl.route('edit-comment/<comment_id>', methods=['POST', 'GET'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    if request.method == 'POST':
        if not comment:
            flash('This post does not exist.', category='error')
        elif comment.author != current_user.id:
            flash('You are not allowed to edit this post.', category='error')
        else:
            new_comment = request.form.get('newComment')
            
            comment.text = new_comment
            comment.edited = True
            db.session.commit()
            flash('Comment has been updated.', category='success')
            
            return redirect(url_for('views.home'))
    else:
        return render_template('edit_comment.html', user=current_user, comment=comment)