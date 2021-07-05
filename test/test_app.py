import os
import tempfile

import pytest
from app import app
from flask import request


@pytest.fixture
def client():
    with app.test_client() as client:
        return client


def test_short_url(client):
    url = 'www.google.com'
    short_url = ''

    response = client.post('/short-urls', json={'original_url': url})
    assert 201 == response.status_code, 'response status should be 201'

    json = response.get_json()
    short_url = json['shorted_key']
    assert url == json['original_url'], "'original_url' in response is wrong"

    response = client.post('/short-urls')
    assert 422 == response.status_code, 'response status should be 422 with no required field'

    short_url = short_url.replace('http://127.0.0.1:5000/', '')
    response = client.get(f'/{short_url}')
    assert 302 == response.status_code, 'response status should be 302'
