import pytest
from rest_framework.test import APIClient
from model_bakery import baker


@pytest.fixture
def api_client():
    return APIClient()
