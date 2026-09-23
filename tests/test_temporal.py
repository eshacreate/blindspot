from core.models import CalendarEvent
from core.temporal import find_temporal_collisions


def test_overlapping_events_are_detected():
    events = [
        CalendarEvent(
            title="Meeting A",
            start="2026-09-24T14:00",
            end="2026-09-24T15:00",
            location="Gujrat",
        ),
        CalendarEvent(
            title="Meeting B",
            start="2026-09-24T14:30",
            end="2026-09-24T16:00",
            location="Lahore",
        ),
    ]

    collisions = find_temporal_collisions(events)

    assert len(collisions) == 1