import os
import tempfile
from fastapi.testclient import TestClient
from src.app import app
from src.db import Base, engine, SessionLocal
from src.models import Activity, Participant

client = TestClient(app)


def setup_module(module):
    # Ensure a fresh database for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    a = Activity(name="Test Activity", description="desc", schedule="now", max_participants=2)
    db.add(a)
    db.commit()
    db.close()


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Test Activity" in data


def test_signup_and_prevent_double():
    res = client.post("/activities/Test Activity/signup", params={"email": "user@example.com"})
    assert res.status_code == 200
    res2 = client.post("/activities/Test Activity/signup", params={"email": "user@example.com"})
    assert res2.status_code == 400


def test_capacity_limit():
    # Fill to capacity
    client.post("/activities/Test Activity/signup", params={"email": "user2@example.com"})
    res = client.post("/activities/Test Activity/signup", params={"email": "user3@example.com"})
    assert res.status_code == 400
