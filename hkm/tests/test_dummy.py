import pytest


@pytest.mark.django_db
def test_dummy(client, default_collection):  # TODO: Add proper tests
    assert client.get('/').status_code == 200
