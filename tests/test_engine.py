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

def test_engine_explains_overlapping_events():
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

    findings = [
        spot for spot in analyze_world(world)
        if spot.type == "Temporal Collision"
    ]

    assert len(findings) == 1
    assert "overlap" in findings[0].problem.lower()
    assert "reschedule" in findings[0].suggested_action.lower()
    assert "Team meeting" in findings[0].evidence[0]
    assert "Doctor appointment" in findings[0].evidence[0]


def test_engine_explains_insufficient_travel_time():
    world = WorldModel(
        events=[
            CalendarEvent(
                title="Meeting in Gulberg",
                start="2026-10-12T10:00",
                end="2026-10-12T11:00",
                location="Gulberg",
            ),
            CalendarEvent(
                title="Meeting in DHA",
                start="2026-10-12T11:15",
                end="2026-10-12T12:00",
                location="DHA",
            ),
        ]
    )

    findings = [
        spot for spot in analyze_world(world)
        if spot.type == "Temporal Collision"
    ]

    assert len(findings) == 1
    assert "travel" in findings[0].problem.lower()
    assert "route" in findings[0].suggested_action.lower()
    assert "15 minutes" in findings[0].evidence[0]
    assert "Gulberg" in findings[0].evidence[0]
    assert "DHA" in findings[0].evidence[0]
