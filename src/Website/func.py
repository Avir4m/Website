import smtplib

def send_email(to_email, msg):
    with open('files/EMAIL.txt', 'r') as f:
        email_sys, password = f.read().split('\n')
        f.close()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sys, password)
    server.sendmail(email_sys, to_email, msg)
    server.quit()
    
def get_secret_key():
    with open("files/SECRET_KEY.txt", "r") as f:
        SECRET_KEY = f.read()
        f.close()
    return SECRET_KEY