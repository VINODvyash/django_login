import uuid
from django.urls import reverse
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_update_profile_success(api_client, create_user):
    user = create_user(username="abcdefgh", email="xyz@gmail.com") #password="pass123")
    api_client.force_authenticate(user=user)

    payload = {
        "username":"abcdefgh",
        #"password":"pass123"
        "email": "xyz@gmail.com"

    }

    response = api_client.put(reverse("update-profile"), payload)

    assert response.status_code == 200
    assert response.data["username"] =="abcdefgh"
    assert response.data["email"] == "xyz@gmail.com"

@pytest.mark.django_db
def test_update_profile_unauthenticated(api_client):
    payload = {
        "username" : "vinod_updated",
        # "password" : "pass123",
        "email" : "xyz@gmail.com"
    }

    response = api_client.put(reverse('update-profile'), payload)

    assert response.status_code == 401
    
@pytest.mark.django_db
def test_update_profile_invalid_data(api_client, create_user):
    user = create_user(username="vinod_updated" )#, email="xyz@gmail.com")
    api_client.force_authenticate(user=user)

    #Invalid password format
    payload = {
        "username" : "vinod_updated",
         "email" : "invalid_email"
        
    }

    response = api_client.put(reverse('update-profile'), payload)

    assert response.status_code == 400
