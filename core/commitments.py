import re

from .models import Commitment


IGNORED_WORDS = {
    "a", "an", "and", "at", "by", "for", "in",
    "of", "on", "the", "to", "with",
}


def normalize_words(text: str) -> set[str]:
    """Extract meaningful words for case- and punctuation-insensitive matching."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {word for word in words if word not in IGNORED_WORDS}


def find_ghost_commitments(
    commitments: list[Commitment],
    planned_actions: list[str],
) -> list[str]:
    ghost_commitments = []

    normalized_actions = [
        normalize_words(action)
        for action in planned_actions
    ]

    for commitment in commitments:
        commitment_words = normalize_words(commitment.text)

        matching_action = bool(commitment_words) and any(
            commitment_words.issubset(action_words)
            for action_words in normalized_actions
        )

        if not matching_action:
            ghost_commitments.append(
                f"Potential ghost commitment: '{commitment.text}'"
            )

    return ghost_commitments
