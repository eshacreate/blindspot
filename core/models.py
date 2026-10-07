from pydantic import BaseModel
from typing import Optional


class CalendarEvent(BaseModel):
    title: str
    start: str
    end: str
    location: Optional[str] = None


class Commitment(BaseModel):
    text: str
    person: Optional[str] = None
    deadline: Optional[str] = None


class BlindSpot(BaseModel):
    type: str
    problem: str
    evidence: list[str]
    confidence: str
    suggested_action: str
class PlannedAction(BaseModel):
    text: str
    completed: bool = False


class WorldModel(BaseModel):
    events: list[CalendarEvent] = []
    commitments: list[Commitment] = []
    planned_actions: list[PlannedAction] = []
    notes: list[str] = []
    locations: list[str] = []
