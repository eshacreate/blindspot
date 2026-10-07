from core.engine import analyze_world
from core.models import CalendarEvent, Commitment, PlannedAction, WorldModel


def test_engine_detects_multiple_blind_spots():
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
        CalendarEvent(
            title="Flight to Islamabad",
            start="2026-09-25T08:00",
            end="2026-09-25T10:00",
            location="Lahore Airport",
        ),
    ]

    commitments = [
        Commitment(
            text="Send the FYP proposal to supervisor",
            person="Supervisor",
            deadline="2026-09-26",
        )
    ]

    planned_actions = []

    world = WorldModel(
        events=events,
        commitments=commitments,
        planned_actions=planned_actions,
    )

    blind_spots = analyze_world(world)

    assert len(blind_spots) == 3
