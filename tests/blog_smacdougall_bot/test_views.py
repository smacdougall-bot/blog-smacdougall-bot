# test_views.py
import pytest

pytestmark = pytest.mark.django_db

def test_index_ok(client):
    # Make a GET request to / and store the response object
    # using a Django test client
    response = client.get('/')
    # Assert that the status_code is 200 (OK)
    assert response.status_code == 200
