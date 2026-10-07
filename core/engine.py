from .models import WorldModel, BlindSpot
from .temporal import find_temporal_collisions
from .commitments import find_ghost_commitments
from .prerequisites import find_missing_prerequisites


def analyze_world(world: WorldModel) -> list[BlindSpot]:

    blind_spots = []

    temporal_results = find_temporal_collisions(world.events)

    for result in temporal_results:
        blind_spots.append(
            BlindSpot(
                type="Temporal Collision",
                problem=result,
                evidence=[result],
                confidence="high",
                suggested_action="Review the timing and allow enough travel time.",
            )
        )

    commitment_results = find_ghost_commitments(
        world.commitments,
        [action.text for action in world.planned_actions],
    )

    for result in commitment_results:
        blind_spots.append(
            BlindSpot(
                type="Ghost Commitment",
                problem=result,
                evidence=[result],
                confidence="medium",
                suggested_action="Create a planned action or reminder for this commitment.",
            )
        )

    prerequisite_results = find_missing_prerequisites(
        world.events,
        world.planned_actions,
    )

    for result in prerequisite_results:
        blind_spots.append(
            BlindSpot(
                type="Prerequisite Failure",
                problem=result,
                evidence=[result],
                confidence="medium",
                suggested_action="Check the required preparation and create a reminder.",
            )
        )

    return blind_spots
