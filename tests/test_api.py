"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient

from backend.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_agent_status():
    """Test agent status endpoint."""
    response = client.get("/api/v1/agents/status")
    assert response.status_code == 200
    assert "seo_agent" in response.json()
