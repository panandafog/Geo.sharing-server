from database.models import Friendship, FriendshipRequest


def make_dict(n):
    return n.to_dict()


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