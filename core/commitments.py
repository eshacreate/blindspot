from .models import Commitment


def find_ghost_commitments(
    commitments: list[Commitment],
    planned_actions: list[str],
) -> list[str]:
    ghost_commitments = []

    for commitment in commitments:
        commitment_text = commitment.text.lower()

        matching_action = any(
            commitment_text in action.lower()
            for action in planned_actions
        )

        if not matching_action:
            ghost_commitments.append(
                f"Potential ghost commitment: '{commitment.text}'"
            )

    return ghost_commitments
