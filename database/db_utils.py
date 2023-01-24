from .db import db
from .models import User


def save_user_location(user_id, latitude, longitude):
    User.objects(id=user_id).update(
        set__latitude=latitude,
        set__longitude=longitude
    )
