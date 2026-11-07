import pytest
from fastapi.testclient import TestClient
from app.main import app, get_interpretation

client = TestClient(app)


def test_health_endpoint():
    """Verify health check returns healthy status and model id."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model" in data


def test_homepage_serves_html():
    """Verify that visiting '/' returns 200 and loads HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "Diabetes Progression Predictor" in response.text


def test_predict_success():
    """Verify prediction endpoint with sample baseline inputs."""
    payload = {
        "age": 0.05,
        "sex": 0.05,
        "bmi": 0.06,
        "bp": 0.02,
        "s1": -0.04,
        "s2": -0.04,
        "s3": -0.02,
        "s4": -0.01,
        "s5": 0.01,
        "s6": 0.02
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_progression_socre" in data
    assert isinstance(data["predicted_progression_socre"], (int, float))
    assert "interpretation" in data
    assert data["interpretation"] in [
        "Below average preogression",
        "Average progression",
        "Above average progression"
    ]


def test_predict_invalid_payload():
    """Verify validation error when required fields are missing or invalid."""
    invalid_payload = {
        "age": "invalid_number",
        "sex": 0.05
    }
    response = client.post("/predict", json=invalid_payload)
    assert response.status_code == 422


def test_interpretation_logic():
    """Unit test for score interpretation categories."""
    assert get_interpretation(80) == "Below average preogression"
    assert get_interpretation(120) == "Average progression"
    assert get_interpretation(190) == "Above average progression"
