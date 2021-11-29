from fastapi.testclient import TestClient
from fastapi import status
from tests.test_auth import TestAuth


class TestUser:
    def test_post(self, client: TestClient):
        payload = {
            "username": "testuser",
            "password": "12345",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "role_id": 1
        }

        access_token = TestAuth().test_login(client)

        response = client.post("/api/users/", json=payload, headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_get_all(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.get("/api/users", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_200_OK

    def test_get(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.get("/api/users/1", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.delete("/api/users/2", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_204_NO_CONTENT
