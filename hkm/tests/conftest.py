import pytest

from kuvaselaamo.tests.conftest import *  # noqa


@pytest.fixture(autouse=True)
def setup_default_from_email(settings):
    settings.DEFAULT_FROM_EMAIL = "kissa@kissa.com"
