import pytest
from fastapi.testclient import TestClient
from tests.conftest import USER_NAME, USER_EMAIL, USER_PHONE, PASSWORD, ROLE


def test_create_user(client):
    data = {
        "name": USER_NAME,
        "email": USER_EMAIL,
        "phone": USER_PHONE,
        "password": PASSWORD,
        "role": ROLE,
    }
    response = client.post("/register", json=data)
    assert response.status_code == 201
    assert "password" not in response.json()
