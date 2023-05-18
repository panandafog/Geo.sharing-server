from tests import conftest
from database.models import User


def test_create_user(test_client):
    response = test_client.post(
        '/user/signup',
        json={
            'username': conftest.user1_username,
            'password': conftest.user1_password,
            'email': conftest.user1_email
        }
    )
    assert response.status_code == 200

    user = User.objects.get(email=conftest.user1_email)
    assert user.username == conftest.user1_username
    assert user.email == conftest.user1_email

def test_login(test_client, auth_user1_id, submit_user1):
    user = User.objects.get(email=conftest.user1_email)
    assert user.email == conftest.user1_email

    response = test_client.post(
        '/user/login',
        json={
            'email': conftest.user1_email,
            'password': conftest.user1_password
        }
    )
    assert response.status_code == 200
    assert response.get_json()['token'] is not None

def test_delete_user(test_client, auth_user1_id, user1_token):
    response = test_client.delete(
        '/user/delete',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
