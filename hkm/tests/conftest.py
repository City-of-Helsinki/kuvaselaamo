import pytest

from hkm.models import Collection


@pytest.fixture
def default_collection(admin_user):
    return Collection.objects.create(
        owner=admin_user,
        show_in_landing_page=True,
    )
