import os
import tempfile

import pytest
from app import app
from flask import request


@pytest.fixture
def client():
    with app.test_client() as client:
        return client


def test_post_short_url(client):
    url = 'www.google.com'
    response = client.post('/short-urls', json={'original_url': url, 'expires_at': '2030-12-31 00:00'})
    assert 201 == response.status_code, 'response status should be 201'

    json = {
        'original_url': url,
        'shorted_key': 'aA1bB2',
        'expires_at': '2020-12-31 00:00'
    }
    response = client.post('/short-urls', json=json)
    assert 201 == response.status_code, 'response status should be 201'

    response = client.post('/short-urls', json={'original_url': url})
    assert 201 == response.status_code, 'response status should be 201'
    assert response.is_json, 'response should be json'

    json = response.get_json()
    assert 'expires_at' in json, "the 'expires_at' should be in the response"
    assert 'original_url' in json, "the 'original_url' should be in the response"
    assert 'shorted_key' in json, "the 'shorted_key' should be in the response"

    short_url = json['shorted_key']
    assert url == json['original_url'], "'original_url' in response is wrong"

    response = client.post('/short-urls')
    assert 422 == response.status_code, 'response status should be 422 with no required field'


def test_get_short_url(client):
    url = 'www.google.com'
    response = client.post('/short-urls', json={'original_url': url})
    short_url = response.get_json()['shorted_key']
    short_url = short_url.replace('http://127.0.0.1:5000/', '')
    response = client.get(f'/{short_url}')
    assert 302 == response.status_code, 'response status should be 302'

    response = client.get(f'/000000')
    assert 404 == response.status_code, 'response status should be 404 with invalid key'


def test_post_login(client):
    credentials = {
        'username': 'admin',
        'password': 'admin',
    }
    response = client.post('/login', json=credentials)
    assert 201 == response.status_code, 'response status should be 201'
    assert response.is_json, 'response should be json'

    json = response.get_json()
    assert 'access_token' in json, "the 'access_token' should be in the response"

    response = client.post('/login', json={'username': 'admin'})
    assert 422 == response.status_code, 'response status should be 422 with no password'

    response = client.post('/login', json={'password': 'admin'})
    assert 422 == response.status_code, 'response status should be 422 with no username'
    
    response = client.post('/login')
    assert 422 == response.status_code, 'response status should be 422 with no values'


def test_get_list_short_urls(client):
    credentials = {
        'username': 'admin',
        'password': 'admin',
    }
    response = client.post('/login', json=credentials)
    assert 201 == response.status_code, 'response status should be 201'

    json = response.get_json()
    access_token = json['access_token']
    response = client.get('/short-urls', headers={'Authorization': f'Bearer {access_token}'})
    assert 200 == response.status_code, 'response status should be 200'

    json = response.get_json()
    assert 'has_next' in json, "the 'has_next' key should be in the response"
    assert 'has_prev' in json, "the 'has_prev' key should be in the response"
    assert 'items' in json, "the 'items' key should be in the response"
    assert 'next_num' in json, "the 'next_num' key should be in the response"
    assert 'page' in json, "the 'page' key should be in the response"
    assert 'pages' in json, "the 'pages' key should be in the response"
    assert 'per_page' in json, "the 'per_page' key should be in the response"
    assert 'prev_num' in json, "the 'prev_num' key should be in the response"
    assert 'total' in json, "the 'total' key should be in the response"
    assert 1 == json['page'], 'the default value for page should be 1'
    assert bool == type(json['has_next']), "type of 'assert 'has_next' should be bool"
    assert bool == type(json['has_prev']), "type of 'assert 'has_prev' should be bool"
    assert int == type(json['page']), "type of 'assert 'page' should be int"
    assert int == type(json['pages']), "type of 'assert 'pages' should be int"
    assert int == type(json['per_page']), "type of 'assert 'per_page' should be int"
    assert int == type(json['total']), "type of 'assert 'total' should be int"
