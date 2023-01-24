from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class User(db.Document):
    username = db.StringField(required=True, unique=True, min_length=5)
    password = db.StringField(required=True, min_length=6)
    latitude = db.FloatField(required=False)
    longitude = db.FloatField(required=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

