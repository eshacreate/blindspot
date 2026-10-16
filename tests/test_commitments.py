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


def test_action_with_extra_timing_words_matches_commitment():
    commitments = [
        Commitment(text="Send the FYP proposal to supervisor")
    ]
    planned_actions = [
        "Send FYP proposal to supervisor tomorrow"
    ]

    assert find_ghost_commitments(commitments, planned_actions) == []


def test_unrelated_action_does_not_match_commitment():
    commitments = [
        Commitment(text="Send the FYP proposal to supervisor")
    ]
    planned_actions = [
        "Buy groceries tomorrow"
    ]

    findings = find_ghost_commitments(commitments, planned_actions)

    assert len(findings) == 1
    assert "FYP proposal" in findings[0]


def test_punctuation_and_capitalization_do_not_prevent_match():
    commitments = [
        Commitment(text="Submit report!")
    ]
    planned_actions = [
        "SUBMIT the report to manager."
    ]

    assert find_ghost_commitments(commitments, planned_actions) == []
