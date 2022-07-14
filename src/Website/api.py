from flask import Blueprint, jsonify


from .models import User, Post, Comment


api = Blueprint('api', __name__)



@api.route('/user/<username>/')
def user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': '404'})
    
    else:
        
        return jsonify({
            'username': f'{user.username}',
            'description': f'{user.description}',
            'picture': f'{user.picture}',
            'posts': len(user.posts),
            'following': len(user.following),
            'followers': len(user.followers)
            })


@api.route('/posts/<username>/')
def posts(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user.id).all()
    if not user:
        return jsonify({'error': '404',
                        'message': f'The username {username} does not exist.'})
        
    elif not posts:
        return jsonify({'error': '404',
                        'message': f'{username} does not have any post.'})
        
    else:         
        return jsonify({'posts': len(user.posts)})


@api.route('/comments/<username>/')
def comments(username):
    user = User.query.filter_by(username=username).first()
    comments = Comment.query.filter_by(author=user.id).all()
    if not user:
        return jsonify({'error': '404',
                        'message': f'{username} does not exist.'})
        
    elif not comments:
        return jsonify({'error': '404',
                        'message': f'{username} does not have any comment.'})
        
    else:
        return jsonify({'comments': len(user.comments)})


@api.route('/post/<username>/<post_id>/')
def post(username, post_id):
    user = User.query.filter_by(username=username).first()
    post = Post.query.filter_by(id=post_id, author=user.id).first()
    if not user:
        return jsonify({'error': '404',
                        'message': f'{username} does not exist.'})

    elif not post:
        return jsonify({'error': '404',
                        'message': 'post does not exist.'})
    
    elif post.private == True:
        return jsonify({'error': '403',
                        'message': 'post is private.'})
        
    else:
        return jsonify({
            'id': f'{post.id}',
            'author': f'{post.user.username}',
            'title': f'{post.title}',
            'text': f'{post.text}',
            'picture': f'{post.picture}',
            'forum': f'{post.forum}',
            'comments': len(post.comments),
            'likes': len(post.likes)
        })