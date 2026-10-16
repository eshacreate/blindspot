from .models import WorldModel, BlindSpot
from .temporal import find_temporal_collisions
from .commitments import find_ghost_commitments
from .prerequisites import find_missing_prerequisites


def analyze_world(world: WorldModel) -> list[BlindSpot]:

    blind_spots = []

    # 1. Temporal collisions
    temporal_results = find_temporal_collisions(world.events)

    for result in temporal_results:
        is_overlap = "overlaps with" in result

        if is_overlap:
            problem = (
                "Two scheduled events overlap in time, so you may not be "
                "able to attend both as planned."
            )
            suggested_action = (
                "Review both commitments and reschedule one if necessary."
            )
        else:
            problem = (
                "There may not be enough time to travel between consecutive "
                "events at different locations."
            )
            suggested_action = (
                "Check the route and realistic travel time. Move one event "
                "or arrange an alternative if the gap is insufficient."
            )

        blind_spots.append(
            BlindSpot(
                type="Temporal Collision",
                problem=problem,
                evidence=[result],
                confidence="high",
                suggested_action=suggested_action,
            )
        )

    # 2. Ghost commitments
    commitment_results = find_ghost_commitments(
        world.commitments,
        [action.text for action in world.planned_actions],
    )

    for result in commitment_results:
        blind_spots.append(
            BlindSpot(
                type="Ghost Commitment",
                problem="You made a commitment that has no matching planned action.",
                evidence=[result],
                confidence="medium",
                suggested_action=(
                    "Create a planned action or reminder for this commitment."
                ),
            )
        )

    # 3. Missing prerequisites
    prerequisite_results = find_missing_prerequisites(
        world.events,
        world.planned_actions,
    )

    for result in prerequisite_results:
        blind_spots.append(
            BlindSpot(
                type="Prerequisite Failure",
                problem="An important preparation step may be missing.",
                evidence=[result],
                confidence="medium",
                suggested_action=(
                    "Check the required preparation and create a reminder."
                ),
            )
        )

    return blind_spots
