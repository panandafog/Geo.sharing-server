import base64
import tempfile

from .db import db
from .models import User, Friendship, FriendshipRequest
from logs import logger


def make_dict(n):
    return n.to_dict()


def save_user_location(user_id, latitude, longitude):
    User.objects(id=user_id).update(
        set__latitude=latitude,
        set__longitude=longitude
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
    # add user2


def search_users(query):
    users_list = User.objects(username=query)
    return list(map(make_dict, users_list))


def get_profile_picture(user_id):
    user = User.objects(id=user_id).first()
    return user.picture.thumbnail.read()


def save_profile_picture(user_id, picture):
    file_like = base64.b64decode(picture.read())
    bytes_image = bytearray(file_like)

    user = User.objects(id=user_id).first()

    with tempfile.TemporaryFile() as file:
        file.write(bytes_image)
        file.flush()
        file.seek(0)
        user.picture.put(file)

    user.save()
