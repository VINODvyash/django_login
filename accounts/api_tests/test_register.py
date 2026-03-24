# import requests 
# # import pytest

# BASE_URL = "http://127.0.0.1:8000/api/"

# def test_register_success():

#     data = {
#         "username": "testuser23",
#         "email": "13testuser1@gmail.com",
#         "password": "3password1234567"
#     }

#     response = requests.post(f"{BASE_URL}register/", json=data)

#     #print(response.json())

#     assert response.status_code == 201

#     # #assert response.json().get("message") == "User registered successfully"

import uuid
from rest_framework.test import APIClient
import pytest

@pytest.mark.django_db
def test_register_success():
    client = APIClient()

    unique_username = f"user_{uuid.uuid4().hex[:6]}"

    data = {
        "username": "unique_username",
        "email": f"{unique_username}@test.com",
        "password": "StrongPass123!"
    }

    response = client.post("/api/register/", data, format="json")

    print(response.data)

    assert response.status_code == 201
