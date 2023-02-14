import smtplib, ssl

import secrets

smtp_server = "smtp.gmail.com"
port = 587
sender_email = secrets.sender_email
password = secrets.password

context = ssl.create_default_context()


def send_email_confirmation_code(user):
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, user.email, str(user.email_confirmation_code))
    server.quit()


def send_password_reset_confirmation_code(user):
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)
    server.login(sender_email, password)
    server.sendmail(sender_email, user.email, str(user.password_reset_code))
    server.quit()
