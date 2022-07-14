import smtplib
import uuid
from email.message import EmailMessage

from . import ALLOWED_EXTENSIONS

def send_email(email_recipient, title, text):
    with open('files/EMAIL.txt', 'r') as f:
        EMAIL_SENDER, PASSWORD = f.read().split('\n')
        f.close()
       
        msg = EmailMessage()
        msg['Subject'] = title
        msg['From'] = EMAIL_SENDER
        msg['To'] = email_recipient
        
        msg.set_content(title)
        
        msg.add_alternative(f"""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1 align="center">{title}</h1>
                <p align="center">{text}</p>
            </body>
        </html>
        """, subtype='html')
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.ehlo()
            smtp.login(EMAIL_SENDER, PASSWORD)
            smtp.send_message(msg)
            smtp.close()
        
        f.close()
    
    
    
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