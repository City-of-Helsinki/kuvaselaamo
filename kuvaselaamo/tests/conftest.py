import pytest
import responses


@pytest.fixture(autouse=True)
def autouse_db(db):
    pass


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps
