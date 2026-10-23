"""API tests use an isolated in-memory SQLite database."""
import os
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"
os.environ["APP_ENV"] = "test"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def _register(email):
    return client.post("/api/v1/auth/register", json={"email": email, "password": "CorrectHorse123"})


def _token(email):
    response = client.post("/api/v1/auth/login", json={"email": email, "password": "CorrectHorse123"})
    return response.json()["access_token"]


def test_register_login_and_me():
    response = _register("trader@example.com")
    assert response.status_code == 201
    token = _token("trader@example.com")
    me = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "trader@example.com"


def test_duplicate_email_and_weak_password():
    _register("duplicate@example.com")
    assert _register("duplicate@example.com").status_code == 409
    assert client.post("/api/v1/auth/register", json={"email": "weak@example.com", "password": "short"}).status_code == 422


def test_auth_required():
    assert client.get("/api/v1/dashboard/summary").status_code == 401


def test_user_only_sees_own_accounts():
    _register("owner1@example.com")
    _register("owner2@example.com")
    token1, token2 = _token("owner1@example.com"), _token("owner2@example.com")
    created = client.post("/api/v1/accounts", headers={"Authorization": f"Bearer {token1}"}, json={
        "label": "Demo MT5", "broker": "Demo Broker", "platform": "MT5",
        "currency": "USD", "equity": "10000", "balance": "9800"
    })
    assert created.status_code == 201
    account_id = created.json()["id"]
    assert len(client.get("/api/v1/accounts", headers={"Authorization": f"Bearer {token1}"}).json()) == 1
    assert client.get("/api/v1/accounts", headers={"Authorization": f"Bearer {token2}"}).json() == []
    assert client.get(f"/api/v1/accounts/{account_id}/positions", headers={"Authorization": f"Bearer {token2}"}).status_code == 404


def test_risk_calculator_route():
    _register("risk@example.com")
    token = _token("risk@example.com")
    response = client.post("/api/v1/risk/position-size", headers={"Authorization": f"Bearer {token}"}, json={
        "equity": "10000", "risk_percent": "1", "entry_price": "100",
        "stop_loss": "95", "value_per_price_unit_per_lot": "1",
        "volume_step": "0.01", "minimum_volume": "0.01"
    })
    assert response.status_code == 200
    from decimal import Decimal
    assert Decimal(response.json()["recommended_volume"]) == Decimal("20.00")
