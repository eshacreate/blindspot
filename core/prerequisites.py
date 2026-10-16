from .models import CalendarEvent, PlannedAction


def find_missing_prerequisites(
    events: list[CalendarEvent],
    planned_actions: list[PlannedAction],
) -> list[str]:
    missing = []

    flights = [
        event for event in events
        if "flight" in event.title.lower()
    ]

    # Completed preparation still counts as preparation.
    action_texts = [
        action.text.lower()
        for action in planned_actions
    ]

    checkin_actions = [
        action for action in action_texts
        if any(term in action for term in ("check-in", "check in", "checkin"))
    ]

    generic_words = {
        "flight", "check", "in", "the", "to", "for",
        "from", "my", "your", "complete", "finish",
    }

    for event in flights:
        title_words = {
            word.strip(".,:;!?()[]{}")
            for word in event.title.lower().split()
        }
        identifiers = title_words - generic_words

        if len(flights) == 1:
            has_checkin = bool(checkin_actions)
        else:
            # With multiple flights, require the check-in action to identify
            # this flight rather than applying one generic action to all.
            has_checkin = any(
                identifiers
                and any(word in action for word in identifiers)
                for action in checkin_actions
            )

        if not has_checkin:
            missing.append(
                f"Potential missing prerequisite for '{event.title}': "
                "no matching check-in action was found."
            )

    return missing
