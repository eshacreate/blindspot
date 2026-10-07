from core.commitments import find_ghost_commitments
from core.models import Commitment


def test_missing_planned_action_is_detected():
    commitments = [
        Commitment(
            text="Send the FYP proposal to supervisor",
            person="Supervisor",
            deadline="2026-09-26",
        )
    ]

    planned_actions = []

    ghost_commitments = find_ghost_commitments(
        commitments,
        planned_actions,
    )

    assert len(ghost_commitments) == 1


def test_existing_planned_action_is_not_flagged():
    commitments = [
        Commitment(
            text="Send the FYP proposal to supervisor",
            person="Supervisor",
            deadline="2026-09-26",
        )
    ]

    planned_actions = [
        "Send the FYP proposal to supervisor"
    ]

    ghost_commitments = find_ghost_commitments(
        commitments,
        planned_actions,
    )

    assert len(ghost_commitments) == 0
