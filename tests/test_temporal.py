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


def test_events_with_insufficient_travel_time_are_detected():
    events = [
        CalendarEvent(
            title="Meeting in Gulberg",
            start="2026-09-24T14:00",
            end="2026-09-24T15:00",
            location="Gulberg",
        ),
        CalendarEvent(
            title="Meeting in DHA",
            start="2026-09-24T15:15",
            end="2026-09-24T16:00",
            location="DHA",
        ),
    ]

    collisions = find_temporal_collisions(events)

    assert len(collisions) == 1
def test_sufficient_travel_time_is_not_flagged():
    events = [
        CalendarEvent(
            title="Meeting in Gulberg",
            start="2026-09-24T14:00",
            end="2026-09-24T15:00",
            location="Gulberg",
        ),
        CalendarEvent(
            title="Meeting in DHA",
            start="2026-09-24T15:45",
            end="2026-09-24T16:30",
            location="DHA",
        ),
    ]

    collisions = find_temporal_collisions(events)

    assert len(collisions) == 0
def test_reverse_order_travel_conflict_is_detected():
    events = [
        CalendarEvent(
            title="Meeting in DHA",
            start="2026-09-24T15:00",
            end="2026-09-24T16:00",
            location="DHA",
        ),
        CalendarEvent(
            title="Meeting in Gulberg",
            start="2026-09-24T16:15",
            end="2026-09-24T17:00",
            location="Gulberg",
        ),
    ]

    collisions = find_temporal_collisions(events)

    assert len(collisions) == 1
