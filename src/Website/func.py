import smtplib
import uuid

from .models import Post, Forum, User
from . import ALLOWED_EXTENSIONS

def send_email(email_recipient, text, sub):
    with open('files/EMAIL.txt', 'r') as f:
        EMAIL_SENDER, PASSWORD = f.read().split('\n')
        f.close()

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_SENDER, PASSWORD)
        subject = sub
        body = text
        msg = f'Subject:{subject}\n\n{body}'
        smtp.sendmail(EMAIL_SENDER, email_recipient, msg)
       

def get_secret_key():
    with open("files/SECRET_KEY.txt", "r") as f:
        SECRET_KEY = f.read()
        f.close()
    return SECRET_KEY


def create_url(type):  
    url = uuid.uuid4().hex
    model = type.query.filter_by(url=url).first()
    if model:
        create_url(type)
    else:
        return url


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
def unique_filename(filename, type):
    new_filename = filename + '_' + uuid.uuid4().hex
    picture = type.query.filter_by(picture=new_filename).first()
    if picture:
        unique_filename(filename)
    else:
        return new_filename