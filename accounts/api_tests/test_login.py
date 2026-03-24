import requests
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.auth import authenticate
from django.urls import reverse


BASE_URL = "http://127.0.0.1:8000/api/"

@pytest.mark.django_db
def test_login_success():
    client = APIClient()

    User.objects.create_user(
        username="vinodiloveyouu",
        password="StrongPass123!"
    )


    payload = {
        "username": "vinodiloveyouu",
        #email="priya@test.com",
        "password": "StrongPass123!"
    }

    response = client.post("/api/login/", payload, format="json")
    # response = client.post(reverse('login'), data)

    
    print("Response Text:", response.text)

    assert response.status_code == 200

    # data = response.json()
    assert "access" in response.data
    assert "refresh" in response.data

    print(response.json())


    