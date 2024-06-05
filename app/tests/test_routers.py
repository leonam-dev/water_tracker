from http import HTTPStatus


def test_create_user_route(client):
    response = client.post('/api/v1/users', json={'name': 'Leonam Raone', 'weight': 70})
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data['name'] == 'Leonam Raone'
    assert data['weight'] == 70
    assert data['daily_goal'] == 2450


def test_create_user_route_invalid_data(client):
    # missing name
    response = client.post('/api/v1/users', json={'weight': 70})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert 'name' in data['message']
    assert 'Missing data for required field.' in data['message']['name']

    # missing weight
    response = client.post('/api/v1/users', json={'name': 'Leonam Raone'})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert 'weight' in data['message']
    assert 'Missing data for required field.' in data['message']['weight']

    # invalid weight
    response = client.post('/api/v1/users', json={'name': 'Leonam Raone', 'weight': -10})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.get_json()
    assert 'weight' in data['message']
    assert 'Weight must be greater than zero.' in data['message']['weight']

