import pytest
from datetime import datetime, timedelta
from hkm.management.commands.clean_unused_data import DEFAULT_DAYS


@pytest.fixture
def day_older_than_removal_date():
    return datetime.today() - timedelta(days=DEFAULT_DAYS + 1)


@pytest.fixture
def day_newer_than_removal_date():
    return datetime.today() - timedelta(days=DEFAULT_DAYS - 1)
