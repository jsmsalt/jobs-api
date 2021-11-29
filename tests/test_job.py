from fastapi.testclient import TestClient
from fastapi import status
from tests.test_auth import TestAuth


class TestJob:
    def test_post(self, client: TestClient):
        payload = {
            "title": "Job Title",
            "text": "Job description",
            "location": "La Rioja"
        }

        access_token = TestAuth().test_login(client)

        response = client.post("/api/jobs/", json=payload, headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_201_CREATED

    def test_get_all(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.get("/api/jobs", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_200_OK

    def test_get(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.get("/api/jobs/1", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_200_OK

    def test_delete(self, client: TestClient):
        access_token = TestAuth().test_login(client)

        response = client.delete("/api/jobs/1", headers={
            'Authorization': f'Bearer {access_token}'
        })

        assert response.status_code == status.HTTP_204_NO_CONTENT
