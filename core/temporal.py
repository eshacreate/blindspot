from datetime import datetime
from .models import CalendarEvent


def format_time(value: datetime) -> str:
    return value.strftime("%I:%M %p").lstrip("0")


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
                    f"{event_a.title} ({format_time(start_a)}–{format_time(end_a)}"
                    f"{' · ' + event_a.location if event_a.location else ''}) "
                    f"overlaps with "
                    f"{event_b.title} ({format_time(start_b)}–{format_time(end_b)}"
                    f"{' · ' + event_b.location if event_b.location else ''})."
                )
                continue

            # Case 2: Not enough travel time between locations
            if end_a <= start_b and event_a.location and event_b.location:
                gap_minutes = (start_b - end_a).total_seconds() / 60

                if event_a.location != event_b.location and gap_minutes < 30:
                    collisions.append(
                        f"{event_a.title} ends at {event_a.location} at "
                        f"{format_time(end_a)}, then {event_b.title} starts at "
                        f"{event_b.location} at {format_time(start_b)} — "
                        f"only {int(gap_minutes)} minutes apart."
                    )

            elif end_b <= start_a and event_a.location and event_b.location:
                gap_minutes = (start_a - end_b).total_seconds() / 60

                if event_a.location != event_b.location and gap_minutes < 30:
                    collisions.append(
                        f"{event_b.title} ends at {event_b.location} at "
                        f"{format_time(end_b)}, then {event_a.title} starts at "
                        f"{event_a.location} at {format_time(start_a)} — "
                        f"only {int(gap_minutes)} minutes apart."
                    )

    return collisions
