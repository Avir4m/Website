from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, abort
from flask_login import login_required, current_user

from .models import Post, Comment
from . import db

comments = Blueprint('comments', __name__)



@comments.route('/create-comment/<post_id>', methods=['POST', 'GET'])
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
            flash('Comment has been created.', category='success')
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))

@comments.route('/delete-comment/<comment_id>/')
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
        flash('Comment has been deleted.', category='success')

    return redirect(url_for('views.home'))

    
@comments.route('/edit-comment/<comment_id>/', methods=['POST', 'GET'])
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
            if new_comment == '':
                flash('Comment cannot be empty.', category='error')
            else:       
                comment.text = new_comment
                comment.edited = True
                db.session.commit()
                flash('Comment has been updated.', category='success')
                return redirect(url_for('views.home'))
                
        return render_template('edit_comment.html', user=current_user, comment=comment)
    else:
        return render_template('edit_comment.html', user=current_user, comment=comment)