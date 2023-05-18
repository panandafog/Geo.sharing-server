from datetime import datetime, timezone
from database.models import User


def make_dict(n):
    return n.to_dict()


def save_user_location(user_id, latitude, longitude):
    User.objects(id=user_id).update(
        set__latitude=latitude,
        set__longitude=longitude,
        set__last_update=datetime.now(timezone.utc)
    )


def search_users(query, user_id):
    users = User.objects(username__icontains=query)
    users_list = list(map(make_dict, users))
    return list(filter(lambda user: str(user['id']) != str(user_id), users_list))