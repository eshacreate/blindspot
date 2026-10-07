from .models import CalendarEvent, PlannedAction


def find_missing_prerequisites(
    events: list[CalendarEvent],
    planned_actions: list[PlannedAction],
) -> list[str]:
    missing = []

    action_texts = [
        action.text.lower()
        for action in planned_actions
        if not action.completed
    ]

    for event in events:
        title = event.title.lower()

        if "flight" in title:
            has_checkin = any(
                "check-in" in action or "check in" in action
                for action in action_texts
            )

            if not has_checkin:
                missing.append(
                    f"Potential missing prerequisite for '{event.title}': "
                    "no check-in action was found."
                )

    return missing
