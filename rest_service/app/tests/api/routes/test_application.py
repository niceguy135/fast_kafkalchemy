from fastapi.testclient import TestClient


def test_create_application(
    client: TestClient
) -> None:
    data = {"user_name": "Jon Doe", "description": "My new application"}
    response = client.post(
        f"/applications/",
        json=data,
    )
    assert response.status_code == 201


def test_new_application_min_name_validation(
    client: TestClient
) -> None:
    data = {"user_name": "", "description": "It must dont work!"}
    response = client.post(
        f"/applications/",
        json=data,
    )
    assert response.status_code == 422


def test_new_application_max_name_validation(
    client: TestClient
) -> None:
    data = {"user_name": "a" * 100, "description": "It must dont work too!"}
    response = client.post(
        f"/applications/",
        json=data,
    )
    assert response.status_code == 422


def test_new_application_max_description_validation(
    client: TestClient
) -> None:
    data = {"user_name": "Jon Doe", "description": "Too looong!" * 20}
    response = client.post(
        f"/applications/",
        json=data,
    )
    assert response.status_code == 422


def test_read_created_application(
    client: TestClient
) -> None:
    data = {"user_name": "Jon Doe", "description": "Read me, pls"}
    client.post(
        f"/applications/",
        json=data,
    )

    response = client.get(
        f"/applications/?username=Jon%20Doe&page=1&size=1"
    )
    assert response.status_code == 200
    assert response.json()["items"][0]["user_name"] == "Jon Doe"


def test_read_application_not_found(
    client: TestClient
) -> None:
    response = client.get(
        f"/applications/?username=Jon%20Doe&page=1&size=1",
    )
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0
