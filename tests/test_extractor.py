import json
from datetime import datetime as RealDateTime
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import core.extractor as extractor


def test_tomorrow_uses_current_pakistan_date(monkeypatch):
    class FrozenDateTime(RealDateTime):
        @classmethod
        def now(cls, tz=None):
            return cls(
                2026, 10, 9, 20, 0,
                tzinfo=tz or ZoneInfo("Asia/Karachi"),
            )

    monkeypatch.setattr(extractor, "datetime", FrozenDateTime)

    captured = {}

    fake_response = {
        "events": [
            {
                "title": "Meeting",
                "start": "2026-10-10T10:00",
                "end": "2026-10-10T11:00",
                "location": None,
            }
        ],
        "commitments": [],
        "planned_actions": [],
        "notes": [],
        "locations": [],
    }

    def fake_create(**kwargs):
        captured["messages"] = kwargs["messages"]
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(fake_response)
                    )
                )
            ]
        )

    monkeypatch.setattr(
        extractor.client.chat.completions,
        "create",
        fake_create,
    )

    world = extractor.extract_context(
        "I have a meeting tomorrow at 10 AM."
    )

    prompt = "\n".join(
        message["content"] for message in captured["messages"]
    )

    assert "Current date: 2026-10-09" in prompt
    assert "2026-10-10" in prompt
    assert world.events[0].start == "2026-10-10T10:00"
    assert world.events[0].end == "2026-10-10T11:00"
