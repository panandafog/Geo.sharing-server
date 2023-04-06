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
    subject = "Your email address confirmation code"
    text = str(user.email_confirmation_code)
    message = 'Subject: {}\n\n{}'.format(subject, text)
    server.sendmail(from_addr=sender_email, to_addrs=user.email, msg=message)
    server.quit()


def send_password_reset_confirmation_code(user):
    server = smtplib.SMTP(smtp_server, port)
    server.starttls(context=context)
    server.login(sender_email, password)
    subject = "Your password change confirmation code"
    text = str(user.password_reset_code)
    message = 'Subject: {}\n\n{}'.format(subject, text)
    server.sendmail(from_addr=sender_email, to_addrs=user.email, msg=message)
    server.quit()
