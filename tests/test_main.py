from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Kickoff API"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"

def test_get_tournaments():
    # This tests connection to Supabase as well
    response = client.get("/tournaments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
