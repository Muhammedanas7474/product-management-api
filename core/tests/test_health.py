import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_endpoint():
    client = APIClient()
    response = client.get("/health/")

    assert response.status_code == 200
    assert "status" in response.data
