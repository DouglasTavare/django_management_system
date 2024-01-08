"""
This module contains fixtures for testing Django REST Framework APIs using the pytest testing 
framework.
The fixtures include an API client and an authenticated API client. The authenticated client is 
set up with a test user, providing a valid access token for testing endpoints that require 
authentication.
"""
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    """
    Fixture to provide an API client for testing.

    :return: APIClient
    """
    yield APIClient()


@pytest.fixture(scope="function")
def authenticated_api_client():
    """
    Fixture to provide an authenticated API client with a valid access token for testing.

    :return: APIClient
    """
    user = User.objects.create_user(username="testuser", password="testpassword")
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return client
