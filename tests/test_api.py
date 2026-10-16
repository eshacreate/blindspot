from fastapi.testclient import TestClient

import app as app_module
from core.models import CalendarEvent, WorldModel


client = TestClient(app_module.app)


def test_analyze_text_returns_structured_blind_spots(monkeypatch):
    world = WorldModel(
        events=[
            CalendarEvent(
                title="Team meeting",
                start="2026-10-12T10:00",
                end="2026-10-12T11:00",
                location="Gujrat",
            ),
            CalendarEvent(
                title="Doctor appointment",
                start="2026-10-12T10:30",
                end="2026-10-12T11:30",
                location="Gujrat",
            ),
        ]
    )

    monkeypatch.setattr(
        app_module,
        "extract_context",
        lambda text: world,
    )

    response = client.post(
        "/analyze-text",
        json={"text": "I have a team meeting and a doctor appointment."},
    )

    assert response.status_code == 200
    findings = response.json()
    assert len(findings) == 1

    finding = findings[0]
    assert finding["type"] == "Temporal Collision"
    assert finding["confidence"] == "high"
    assert finding["evidence"]
    assert finding["problem"]
    assert finding["suggested_action"]


def test_analyze_text_rejects_empty_input():
    response = client.post("/analyze-text", json={"text": ""})

    assert response.status_code == 422


def test_analyze_text_rejects_whitespace_only_input():
    response = client.post("/analyze-text", json={"text": "   "})

    assert response.status_code == 422


def test_analyze_text_rejects_missing_text_field():
    response = client.post("/analyze-text", json={})

    assert response.status_code == 422


def test_analyze_text_returns_safe_error_when_extraction_fails(monkeypatch):
    def fail_extraction(text):
        raise RuntimeError("Private upstream diagnostic")

    monkeypatch.setattr(app_module, "extract_context", fail_extraction)

    response = client.post(
        "/analyze-text",
        json={"text": "I have a meeting tomorrow."},
    )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "BlindSpot could not analyze this text right now. Please try again."
    )
    assert "Private upstream diagnostic" not in response.text


def test_analyze_text_rejects_oversized_input():
    response = client.post(
        "/analyze-text",
        json={"text": "x" * 10001},
    )

    assert response.status_code == 422
