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

            # Case 1: Events directly overlap
            if start_a < end_b and start_b < end_a:
                collisions.append(
                    f"'{event_a.title}' overlaps with '{event_b.title}'."
                )
                continue

            # Case 2: Events are back-to-back but locations differ
            # and there may not be enough time to travel.
            if end_a <= start_b and event_a.location and event_b.location:
                gap_minutes = (start_b - end_a).total_seconds() / 60

                if event_a.location != event_b.location and gap_minutes < 30:
                    collisions.append(
                        f"'{event_a.title}' ends at {event_a.location}, "
                        f"then '{event_b.title}' starts at {event_b.location} "
                        f"only {int(gap_minutes)} minutes later."
                    )

            elif end_b <= start_a and event_a.location and event_b.location:
                gap_minutes = (start_a - end_b).total_seconds() / 60

                if event_a.location != event_b.location and gap_minutes < 30:
                    collisions.append(
                        f"'{event_b.title}' ends at {event_b.location}, "
                        f"then '{event_a.title}' starts at {event_a.location} "
                        f"only {int(gap_minutes)} minutes later."
                    )

    return collisions