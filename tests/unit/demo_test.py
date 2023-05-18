from database.models import User

def test_new_user():
    user = User(username='username', password='password', email='email')
    assert user.username == 'username'
