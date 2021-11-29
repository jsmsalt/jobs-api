from fastapi.testclient import TestClient
from fastapi import status
from tests.test_auth import TestAuth


class TestSession:
    def test_post(self, client: TestClient):
        payload = {
            "access_token": "abcdefghi",
            "ip_address": None,
            "user_agent": None,
            "user_id": 1
        }

        access_token = TestAuth().test_login(client)

        response = client.post("/api/sessions/", json=payload, headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_get_all(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.get("/api/sessions", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_200_OK

    def test_get(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.get("/api/sessions/1", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.delete("/api/sessions/1", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_204_NO_CONTENT
