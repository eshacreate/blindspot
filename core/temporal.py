from datetime import datetime
from .models import CalendarEvent


def find_temporal_collisions(events: list[CalendarEvent]) -> list[str]:
    collisions = []

    parsed_events = [
        (
            event,
            datetime.fromisoformat(event.start),
            datetime.fromisoformat(event.end),
        )
        for event in events
    ]

    for i, (event_a, start_a, end_a) in enumerate(parsed_events):
        for event_b, start_b, end_b in parsed_events[i + 1:]:
            if start_a < end_b and start_b < end_a:
                collisions.append(
                    f"'{event_a.title}' overlaps with '{event_b.title}'."
                )

    return collisions