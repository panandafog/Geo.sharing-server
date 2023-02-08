import smtplib, ssl

import secrets

smtp_server = "smtp.gmail.com"
port = 587
sender_email = secrets.sender_email
password = secrets.password

context = ssl.create_default_context()

server = smtplib.SMTP(smtp_server, port)
server.starttls(context=context)  # Secure the connection
server.login(sender_email, password)

def send_email_confirmation_code(user):
    server.sendmail(sender_email, user.email, str(user.email_confirmation_code))


def send_password_reset_confirmation_code(user):
    server.sendmail(sender_email, user.email, str(user.password_reset_code))
