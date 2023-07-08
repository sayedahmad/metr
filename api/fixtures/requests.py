import pytest
from rest_framework.test import APIClient


@pytest.fixture(scope="function")
def unauthenticated_client(db_session):
    client = APIClient()
    yield client
