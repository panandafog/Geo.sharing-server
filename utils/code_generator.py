from random import randint


def email_confirmation_code():
    return str(randint(100000, 999999))


def password_reset_code():
    return str(randint(100000, 999999))
