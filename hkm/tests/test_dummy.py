import pytest

@pytest.mark.django_db
def test_dummy(client):
    # TODO: Add proper tests
    try:
        client.get('/')
    except:
        pass
