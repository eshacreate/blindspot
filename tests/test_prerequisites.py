from core.models import CalendarEvent, PlannedAction
from core.prerequisites import find_missing_prerequisites


def test_missing_flight_checkin_is_detected():
    events = [
        CalendarEvent(
            title="Flight to Islamabad",
            start="2026-09-25T08:00",
            end="2026-09-25T10:00",
            location="Lahore Airport",
        )
    ]

    planned_actions = []

    missing = find_missing_prerequisites(
        events,
        planned_actions,
    )

    assert len(missing) == 1


def test_existing_flight_checkin_is_not_flagged():
    events = [
        CalendarEvent(
            title="Flight to Islamabad",
            start="2026-09-25T08:00",
            end="2026-09-25T10:00",
            location="Lahore Airport",
        )
    ]

    planned_actions = [
        PlannedAction(
            text="Complete flight check-in"
        )
    ]

    missing = find_missing_prerequisites(
        events,
        planned_actions,
    )

    assert len(missing) == 0


def test_checkin_for_one_flight_does_not_cover_another():
    events = [
        CalendarEvent(
            title="Flight to Islamabad",
            start="2026-10-12T08:00",
            end="2026-10-12T10:00",
            location="Lahore Airport",
        ),
        CalendarEvent(
            title="Flight to Karachi",
            start="2026-10-13T09:00",
            end="2026-10-13T11:00",
            location="Lahore Airport",
        ),
    ]
    planned_actions = [
        PlannedAction(text="Check-in for flight to Islamabad")
    ]

    missing = find_missing_prerequisites(events, planned_actions)

    assert len(missing) == 1
    assert "Flight to Karachi" in missing[0]


def test_completed_checkin_counts_as_preparation():
    events = [
        CalendarEvent(
            title="Flight to Islamabad",
            start="2026-10-12T08:00",
            end="2026-10-12T10:00",
            location="Lahore Airport",
        )
    ]
    planned_actions = [
        PlannedAction(
            text="Complete flight check-in",
            completed=True,
        )
    ]

    assert find_missing_prerequisites(events, planned_actions) == []


def test_non_flight_event_needs_no_flight_checkin():
    events = [
        CalendarEvent(
            title="Team meeting",
            start="2026-10-12T10:00",
            end="2026-10-12T11:00",
            location="Gujrat",
        )
    ]

    assert find_missing_prerequisites(events, []) == []
