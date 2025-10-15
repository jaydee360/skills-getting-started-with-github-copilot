import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_signup_and_unregister():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "pytestuser@mergington.edu"

    # Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Unregister
    unregister_resp = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert f"Unregistered {email}" in unregister_resp.json()["message"]


def test_signup_duplicate():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "pytestdup@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Try duplicate signup
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]
    # Cleanup
    client.delete(f"/activities/{activity_name}/unregister?email={email}")


def test_unregister_not_signed_up():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "pytestnotfound@mergington.edu"
    resp = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert resp.status_code == 400
    assert "not registered" in resp.json()["detail"]
