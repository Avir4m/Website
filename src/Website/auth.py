from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import SignatureExpired, URLSafeTimedSerializer
import smtplib

from . import db
from .models import User

auth = Blueprint('auth', __name__)

with open("files/SECRET_KEY.txt", "r") as f:
    SECRET_KEY = f.read()
    f.close()

s = URLSafeTimedSerializer(SECRET_KEY)

def send_email(email, msg):
    with open('files/EMAIL.txt', 'r') as f:
        email_sys, password = f.read().split('\n')
        f.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sys, password)
    server.sendmail(email_sys, email, msg)
    server.quit()



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
                flash('Invalid password, Please try again.', category='error')
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
        else:
            new_user = User(email=email, username=username ,first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method='sha256'), verified=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            
            #Send verifaction email
            token = s.dumps(email, salt='email-confirm')
            link = url_for('auth.confirm_email', token=token, _external=True)
            msg = f'Email confirmation\n {link}'
            send_email(email, msg)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template('signup.html', user=current_user)
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
            msg = f'Email confirmation\n {link}'
            send_email(email, msg)
            flash('Sent a verification link to your email address', category='success')
        else:
            flash('This email is not connected to any account, please try different email addresses.', category='error')
        
    return render_template('forgot_password.html', user=current_user)

@auth.route('/verify_email/')
def verify_email():
    user = current_user
    email = user.email

    token = s.dumps(email, salt='email-confirm')
    link = url_for('auth.confirm_email', token=token, _external=True)
    msg = f'Email confirmation\n {link}'
    send_email(email, msg)
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
        
       