from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired, URLSafeTimedSerializer

from . import db
from .models import User, Post, Comment, Like, Saved
from .func import send_email, get_secret_key

auth = Blueprint('auth', __name__)

SECRET_KEY = get_secret_key()

s = URLSafeTimedSerializer(SECRET_KEY)


# Auth

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if 'check' in request.form:
            remember = True
        else:
            remember = False
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=remember)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password or email address, Please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
        
    return render_template('login.html', user=current_user)


@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))    


@auth.route('/sign-up/', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('userName')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user_email = User.query.filter_by(email=email).first()
        user_name = User.query.filter_by(username=username).first()
        
        if user_email:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif user_name:
            flash('Username already exists.', category='error')
        elif username == '':
            flash('You must provide a username.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 6 characters.', category='error')
        elif ' ' in username:
            flash('You cannot have spaces in username.', category='error')
        else:
            new_user = User(email=email, username=username ,first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('signup.html', user=current_user)

# Password

@auth.route('/change_password/', methods=['POST', 'GET'])
@login_required
def change_password():
    if request.method == 'POST':
        
        email = current_user.email
        
        user = User.query.filter_by(email=email).first()
        
        password = request.form.get('password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if check_password_hash(user.password, password):
            if password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif check_password_hash(user.password, password1):
                flash('New password can\'t be the same as the old one.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 6 characters.', category='error')
            else:
                current_user.password = generate_password_hash(password1, method='sha256')
                db.session.commit()
                flash('Password has been changed!', category='success')
                return redirect(url_for('views.dashboard'))
        else:
            flash('Invalid password, Please try again.', category='error')
            
    return render_template('change_password.html', user=current_user)

@auth.route('/forgot_password/', methods=['POST', 'GET'])
def forgot_password():
    if request.method == 'POST':
        
        email = request.form.get('email')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            token = s.dumps(email, salt='reset-password')
            link = url_for('auth.reset_password', token=token, _external=True)
            msg = f'Email confirmation:\n {link}'
            sub = 'Email confirmation'
            send_email(email, msg, sub)
            flash('Sent a verification link to your email address', category='success')
        else:
            flash('This email is not connected to any account, please try different email addresses.', category='error')
        
    return render_template('forgot_password.html', user=current_user)


@auth.route('/reset_password/<token>/', methods=['POST', 'GET'])
def reset_password(token):
    try:
        email = s.loads(token, salt='reset-password', max_age=600) # 600 Seconds (10 minutes)
        user = User.query.filter_by(email=email).first()
        if user:
            if request.method == 'POST':
                password1 = request.form.get('password1')
                password2 = request.form.get('password2')
                
                if password1 != password2:
                    flash('Passwords don\'t match..', category='error')
                elif len(password1) < 7:
                    flash('Password must be at least 6 characters.', category='error')
                elif check_password_hash(user.password, password1):
                    flash('New password can\'t be the same as the old one.', category='error')
                else:
                    user.password = generate_password_hash(password1, method='sha256')
                    db.session.commit()
                    flash('Password has been changed!', category='success')
                    return redirect(url_for('views.home'))
                return render_template('reset_password.html', user=current_user)
            else:
                return render_template('reset_password.html', user=current_user)
        else:
            flash('Invalid token', category='error')
    except SignatureExpired:
        abort(404)
        
# Email

@auth.route('/verify_email/')
def verify_email():
    user = current_user
    email = user.email

    token = s.dumps(email, salt='email-confirm')
    link = url_for('auth.confirm_email', token=token, _external=True)
    msg = f'Email confirmation\n {link}'
    sub = 'Email confirmation'
    send_email(email, msg, sub)
    return redirect(url_for('views.dashboard', username=user.username))

@auth.route('/confirm_email/<token>/')
@login_required
def confirm_email(token):
    user = current_user
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600) # 3600 Seconds (1 Hour)
        if email == user.email:
            user.verified = True
            db.session.commit()
            flash('Account is now verified!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Invalid token', category='error')
    except SignatureExpired:
       abort(404)

# User

@auth.route('/delete-user/<user_id>/', methods=['POST', 'GET'])
@login_required
def delete_user(user_id):
    per = current_user.permissions # Permissions
    if per >= 1:
        user =  User.query.filter_by(id=user_id).first()
        Post.query.filter_by(author=user.id).delete()
        Comment.query.filter_by(author=user.id).delete()
        Like.query.filter_by(author=user.id).delete()
        Saved.query.filter_by(author=user.id).delete()
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.id} has been deleted!', category='success')
        return redirect(url_for('admin.users'))
    else:
        if int(user_id) == int(current_user.id):
            user = current_user
            email = user.email
            token = s.dumps(email, salt='delete-user-confirm')
            link = url_for('auth.confirm_user_delete', token=token, _external=True)
            msg = f'Delete user confirmation\n {link}'
            sub = 'Delete User Confirmation'
            send_email(email, msg, sub)
            flash(f'We have sent you confirmation link to your email address.', category='success')
            return redirect(url_for('views.dashboard', username=user.username))
        else:
            flash('You are not allowed to delete other users')
            abort(403)
            
@auth.route('/confirm-user-delete/<token>/')
@login_required
def confirm_user_delete(token):
    user = current_user
    try:
        email = s.loads(token, salt='delete-user-confirm', max_age=86400) # 86400 Seconds (24 Hours)
        if email == user.email:
            user = User.query.filter_by(id=user.id).first()
            Post.query.filter_by(author=user.id).delete()
            Comment.query.filter_by(author=user.id).delete()
            Like.query.filter_by(author=user.id).delete()
            Saved.query.filter_by(author=user.id).delete()
            db.session.delete(user)
            db.session.commit()
            flash('Account has been deleted!', category='success')
            return redirect(url_for('auth.sign_up'))
        else:
            flash('Invalid token', category='error')
    except SignatureExpired:
       abort(404)
