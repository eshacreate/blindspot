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
