from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

import utils.code_generator as code_generator


class User(db.Document):
    username = db.StringField(required=True, unique=True, min_length=6)
    email = db.StringField(required=True, unique=True, min_length=6)
    password = db.StringField(required=True, min_length=6)

    email_confirmation_code = db.StringField()
    password_reset_code = db.StringField()

    latitude = db.FloatField(required=False)
    longitude = db.FloatField(required=False)

    picture = db.ImageField(thumbnail_size=(300, 300, False))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def generate_email_confirmation_code(self):
        self.email_confirmation_code = code_generator.email_confirmation_code()

    def generate_password_reset_code(self):
        self.password_reset_code = code_generator.password_reset_code()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_confirmed(self):
        return self.email_confirmation_code is None

    def to_dict(self):
        return {
            "id": str(self.pk),
            "username": self.username,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


class FriendshipRequest(db.Document):
    sender = db.ReferenceField(User)
    recipient = db.ReferenceField(User)

    def to_dict(self):
        return {
            "id": str(self.pk),
            "sender": self.sender.to_dict(),
            "recipient": self.recipient.to_dict()
        }


class Friendship(db.Document):
    user1 = db.ReferenceField(User)
    user2 = db.ReferenceField(User)

    def to_dict(self):
        return {
            "id": str(self.pk),
            "user1": self.user1.to_dict(),
            "user2": self.user2.to_dict()
        }
