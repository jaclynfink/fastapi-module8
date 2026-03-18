import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_read_root_returns_html(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Hello World" in response.text


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize(
    "endpoint,payload,expected",
    [
        ("/add", {"a": 2, "b": 3}, 5),
        ("/subtract", {"a": 5, "b": 3}, 2),
        ("/multiply", {"a": 2, "b": 4}, 8),
        ("/divide", {"a": 9, "b": 3}, 3.0),
    ],
)
def test_operation_endpoints_success(client, endpoint, payload, expected):
    response = client.post(endpoint, json=payload)

    assert response.status_code == 200
    assert response.json() == {"result": expected}


@pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
def test_operation_endpoints_validation_error(client, endpoint):
    response = client.post(endpoint, json={"a": "not-a-number", "b": 2})

    assert response.status_code == 400
    body = response.json()
    assert "error" in body
    assert "a" in body["error"]


def test_divide_by_zero_returns_error(client):
    response = client.post("/divide", json={"a": 5, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"error": "Cannot divide by zero!"}
