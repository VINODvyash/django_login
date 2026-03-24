import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

user = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def make_user(**kwargs):
        return user.objects.create_user(**kwargs)
    return make_user