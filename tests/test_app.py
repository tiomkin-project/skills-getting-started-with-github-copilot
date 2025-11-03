import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_delete_participant():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Signup
    resp_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {email}" in resp_signup.json()["message"]
    # Try duplicate signup
    resp_dup = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp_dup.status_code == 400
    # Delete participant
    resp_del = client.delete(f"/activities/{activity_name}/participant?email={email}")
    assert resp_del.status_code == 200
    assert f"Removed {email}" in resp_del.json()["message"]
    # Try deleting again
    resp_del2 = client.delete(f"/activities/{activity_name}/participant?email={email}")
    assert resp_del2.status_code == 404
