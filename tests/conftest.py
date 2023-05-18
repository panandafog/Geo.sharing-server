import pytest
import datetime
from flask_jwt_extended import create_access_token

import configuration.configurator as configuration
import services.users as users_service
import services.authorization as authorization_service
from app import create_app
from database.models import drop_all
from database.models import User

user1_username = 'user1_username'
user1_password = 'user1_password'
user1_email = 'user1@email.com'

user2_username = 'user2_username'
user2_password = 'user2_password'
user2_email = 'user2@email.com'

@pytest.fixture(scope='session')
def test_app():
    configuration.set_testing(True)
    app = create_app()
    yield app

@pytest.fixture(scope='session')
def test_client_(test_app):
    with test_app.test_client() as test_client:
        yield test_client

@pytest.fixture(scope='function')
def test_client(test_app, test_client_):
    drop_all()
    yield test_client_
    drop_all()

@pytest.fixture(scope='function')
def auth_user1_id(test_client):
    yield authorization_service.signup(user1_username, user1_password, user1_email)

@pytest.fixture(scope='function')
def submit_user1(test_client, auth_user1_id):
    yield User.objects(username=user1_username).update(
        set__email_confirmation_code=None
    )

@pytest.fixture(scope='function')
def user1_token(test_client, auth_user1_id, submit_user1):
    access_token = create_access_token(
        identity=str(auth_user1_id),
        expires_delta=datetime.timedelta(days=1)
    )
    yield access_token

@pytest.fixture(scope='function')
def auth_user2_id(test_client):
    yield authorization_service.signup(user2_username, user2_password, user2_email)

@pytest.fixture(scope='function')
def submit_user2(test_client, auth_user2_id):
    yield User.objects(username=user2_username).update(
        set__email_confirmation_code=None
    )

@pytest.fixture(scope='function')
def user2_token(test_client, auth_user2_id, submit_user2):
    access_token = create_access_token(
        identity=str(auth_user2_id),
        expires_delta=datetime.timedelta(days=1)
    )
    yield access_token
