from database.models import User


def get_profile_picture(user_id):
    user = User.objects(id=user_id).first()
    return user.picture.thumbnail.read()


def save_profile_picture(user_id, picture):
    user = User.objects(id=user_id).first()
    user.picture.delete()
    user.picture.put(picture)
    user.save()


def delete_profile_picture(user_id):
    user = User.objects(id=user_id).first()
    user.picture.delete()
    user.save()