"""Global project fixtures."""

import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """Return API client."""
    return APIClient()


@pytest.fixture
def user_payload():
    """Return sample user information as a payload."""
    return {
        "email": "user@example.com",
        "password": "test_pass123",
    }


@pytest.fixture
def sample_user(user_payload):
    """Create and return a sample user."""
    return baker.make(User, **user_payload)


@pytest.fixture
def sample_admin(user_payload):
    """Create and return a sample admin user."""
    return baker.make(User, is_staff=True, **user_payload)
