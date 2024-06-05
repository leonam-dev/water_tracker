import uuid, pytz

from http import HTTPStatus
from datetime import datetime


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


def test_add_intake_route(client, test_user):
    response = client.post(f'/api/v1/users/{test_user.id}/intakes', json={'amount': 500})
    assert response.status_code == HTTPStatus.CREATED
    data = response.get_json()
    assert data['amount'] == 500


def test_add_intake_invalid_data(client, test_user):
    # missing amount
    response = client.post(f'/api/v1/users/{test_user.id}/intakes', json={'user_id': test_user.id})
    assert response.status_code == HTTPStatus.BAD_REQUEST

    # invalid amount
    response = client.post(f'/api/v1/users/{test_user.id}/intakes', json={'amount': -500})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_intake_route(client, test_user):
    date = datetime.now(pytz.timezone('America/Sao_Paulo')).date().strftime('%d-%m-%Y')
    client.post(f'/api/v1/users/{test_user.id}/intakes', json={'amount': 500})
    response = client.get(f'/api/v1/users/{test_user.id}/intakes?date={date}')
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data['total_intake'] == 500


def test_get_intake_user_not_found(client):
    date = datetime.now(pytz.timezone('America/Sao_Paulo')).date().strftime('%d-%m-%Y')
    response = client.get(f'/api/v1/users/{uuid.uuid4()}/intakes?date={date}')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_intakes_history_route(client, test_user):
    client.post(f'/api/v1/users/{test_user.id}/intakes', json={'amount': 500})
    client.post(f'/api/v1/users/{test_user.id}/intakes', json={'amount': 1000})
    response = client.get(f'/api/v1/users/{test_user.id}/intakes-history')
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['total_intake'] == 1500
