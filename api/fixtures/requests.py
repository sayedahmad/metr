from rest_framework.test import APIClient
import pytest


@pytest.fixture(scope="function")
def unauthenticated_client(db_session):
    client = APIClient()
    yield client
