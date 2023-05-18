from logs import logger
from utils import email_helper
from utils.exceptions import APIException
from database.models import User
import services.pictures as pictures

def signup(username, password, email):
    user = User(username=username, password=password, email=email)
    user.hash_password()
    user.generate_email_confirmation_code()

    users_with_same_username = User.objects(username=username, email__ne=email)
    if len(users_with_same_username) > 0:
        raise APIException(406, "Username is already taken")

    users_with_same_email = User.objects(username__ne=username, email=email)
    if len(users_with_same_email) > 0:
        raise APIException(406, "Email is already taken")

    same_user = User.objects(username=username, email=email).first()
    if not (same_user is None):
        if same_user.is_confirmed():
            logger.log(str(same_user.email_confirmation_code))
            logger.log(str(same_user.email_confirmation_code is None))
            logger.log(str(same_user.is_confirmed()))
            raise APIException(406, "User already exists")
        else:
            same_user.delete()

    user.save()
    email_helper.send_email_confirmation_code(user)
    return user.id


def confirm_email(user_id, code):
    user = User.objects(id=user_id).first()
    if user is None:
        raise ValueError("user not found")
    if str(user.email_confirmation_code) != str(code):
        raise ValueError("wrong code")
    user.email_confirmation_code = None
    user.save()
    return user.id


def request_password_change(email):
    user = User.objects(email=email).first()
    if user is None:
        raise ValueError("user not found")
    user.generate_password_reset_code()
    user.save()
    email_helper.send_password_reset_confirmation_code(user)
    return user.id


def change_password(email, code, new_password):
    user = User.objects(email=email).first()
    if user is None:
        raise ValueError("user not found")
    if str(user.password_reset_code) != str(code):
        raise ValueError("wrong code")
    user.password_reset_code = None
    user.password = new_password
    user.hash_password()
    user.save()


def validate_user(user_id):
    user = User.objects(id=user_id).first()
    if user is None:
        raise APIException.unauthorized("User not found")
    if not user.is_confirmed():
        raise APIException.unauthorized("User's email is not confirmed")


def delete_user(user_id):
    pictures.delete_profile_picture(user_id)
    User.objects(id=user_id).delete()
