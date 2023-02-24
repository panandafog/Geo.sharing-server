import base64
import tempfile

from .db import db
from datetime import datetime, timezone
from .models import User, Friendship, FriendshipRequest
from logs import logger
from utils import email_helper
from utils.exceptions import APIException


def make_dict(n):
    return n.to_dict()


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
    if not user.is_confirmed():
        raise ValueError("user's email is not confirmed")


def save_user_location(user_id, latitude, longitude):
    User.objects(id=user_id).update(
        set__latitude=latitude,
        set__longitude=longitude,
        set__last_update=datetime.now(timezone.utc)
    )


def create_friendship_request(sender_id, recipient_id):
    existing_requests_list = FriendshipRequest.objects(sender=sender_id, recipient=recipient_id)
    if len(existing_requests_list) > 0:
        raise ValueError("request already exists")
    FriendshipRequest(sender=sender_id, recipient=recipient_id).save()


def delete_friendship_request(sender_id, recipient_id):
    FriendshipRequest.objects(sender=sender_id, recipient=recipient_id).delete()


def accept_friendship_request(sender_id, recipient_id):
    add_friendship(sender_id, recipient_id)
    delete_friendship_request(sender_id, recipient_id)


def reject_friendship_request(sender_id, recipient_id):
    delete_friendship_request(sender_id, recipient_id)


def get_incoming_friendship_requests(user_id):
    requests_list = FriendshipRequest.objects(recipient=user_id)
    result = list(map(make_dict, requests_list))
    return result


def get_outgoing_friendship_requests(user_id):
    requests_list = FriendshipRequest.objects(sender=user_id)
    result = list(map(make_dict, requests_list))
    return result


def add_friendship(user_id_1, user_id_2):
    existing_friendships_list = Friendship.objects(user1=user_id_1, user2=user_id_2)
    if len(existing_friendships_list) > 0:
        raise ValueError("friends already exist")
    Friendship(user1=user_id_1, user2=user_id_2).save()


def delete_friendship(user_id_1, user_id_2):
    Friendship.objects(user1=user_id_1, user2=user_id_2).delete()
    Friendship.objects(user1=user_id_2, user2=user_id_1).delete()


def get_friends(user_id):
    friendships_list_1 = Friendship.objects(user1=user_id)
    friendships_list_2 = Friendship.objects(user2=user_id)
    result = list(map(make_dict, friendships_list_1)) + list(map(make_dict, friendships_list_2))
    return result


def search_users(query, user_id):
    users = User.objects(username__icontains=query)
    users_list = list(map(make_dict, users))
    return list(filter(lambda user: str(user['id']) != str(user_id), users_list))


def get_profile_picture(user_id):
    user = User.objects(id=user_id).first()
    return user.picture.thumbnail.read()


def save_profile_picture(user_id, picture):
    user = User.objects(id=user_id).first()
    user.picture.delete()
    user.picture.put(picture)
    user.save()
