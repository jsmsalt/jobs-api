import pytest
from settings import Settings
from fastapi.testclient import TestClient
from fastapi import status

settings = Settings()


class TestAuth:
    def test_login(self, client: TestClient):

        if pytest.access_token:
            return pytest.access_token

        credentials = {
            'username': 'admin',
            'password': settings.admin_password
        }

        response = client.post("/api/auth/login", json=credentials)
        json_response = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in json_response

        pytest.access_token = json_response['access_token']

        return pytest.access_token

    def test_login_wrong_password(self, client: TestClient):

        credentials = {
            'username': 'admin',
            'password': 'wrong_password'
        }

        response = client.post("/api/auth/login", json=credentials)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout(self, client: TestClient):
        access_token = self.test_login(client)

        response = client.post(
            "/api/auth/logout",
            headers={'Authorization': f'Bearer {access_token}'}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        pytest.access_token = None
