import pytest


@pytest.mark.django_db
@pytest.mark.xfail  # TODO: Add proper tests
def test_dummy(client):
    client.get('/')
