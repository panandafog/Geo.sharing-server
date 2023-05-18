import json


def test_create_friendship(test_client, auth_user1_id, user1_token, auth_user2_id, user2_token):
    response = test_client.post(
        '/friendship/create_request',
        json={'recipient_id': str(auth_user2_id)},
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200

    response = test_client.get(
        '/friendship/get_incoming_requests',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friendship/get_outgoing_requests',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert json.loads(response.text)[0]['sender']['id'] == str(auth_user1_id)
    assert json.loads(response.text)[0]['recipient']['id'] == str(auth_user2_id)

    response = test_client.get(
        '/friendship/get_incoming_requests',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert json.loads(response.text)[0]['sender']['id'] == str(auth_user1_id)
    assert json.loads(response.text)[0]['recipient']['id'] == str(auth_user2_id)

    response = test_client.get(
        '/friendship/get_outgoing_requests',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0


def test_accept_friendship(test_client, auth_user1_id, user1_token, auth_user2_id, user2_token):
    response = test_client.post(
        '/friendship/create_request',
        json={'recipient_id': str(auth_user2_id)},
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200

    response = test_client.post(
        '/friendship/accept_request',
        json={'sender_id': str(auth_user1_id)},
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200

    response = test_client.get(
        '/friendship/get_incoming_requests',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friendship/get_outgoing_requests',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friendship/get_incoming_requests',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friendship/get_outgoing_requests',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friends/get',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 1

    response = test_client.get(
        '/friends/get',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 1

def test_reject_friendship(test_client, auth_user1_id, user1_token, auth_user2_id, user2_token):
    response = test_client.post(
        '/friendship/create_request',
        json={'recipient_id': str(auth_user2_id)},
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200

    response = test_client.post(
        '/friendship/reject_request',
        json={'sender_id': str(auth_user1_id)},
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200

    response = test_client.get(
        '/friendship/get_incoming_requests',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friendship/get_outgoing_requests',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friendship/get_incoming_requests',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friendship/get_outgoing_requests',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friends/get',
        headers={'Authorization': 'Bearer ' + str(user1_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0

    response = test_client.get(
        '/friends/get',
        headers={'Authorization': 'Bearer ' + str(user2_token)}
    )
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 0
