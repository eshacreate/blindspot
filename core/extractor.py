import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from groq import Groq

from .models import WorldModel, CalendarEvent, Commitment, PlannedAction

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_context(text: str) -> WorldModel:
    today = datetime.now(ZoneInfo("Asia/Karachi")).date()
    tomorrow = today + timedelta(days=1)
    prompt = f"""
You are the context extraction component of BlindSpot,
an omission-detection system.

Extract ONLY information explicitly supported by the user's text.

Return valid JSON with exactly these fields:

{{
  "events": [],
  "commitments": [],
  "planned_actions": [],
  "notes": [],
  "locations": []
}}

Event format:
{{
  "title": "...",
  "start": "YYYY-MM-DDTHH:MM",
  "end": "YYYY-MM-DDTHH:MM",
  "location": "..."
}}
Event rules:
- If the user gives only a start time, infer a reasonable duration:
  meetings = 60 minutes
  flights = 120 minutes
- Never make start and end identical unless the event is truly instantaneous.
- For "tomorrow", use {tomorrow.isoformat()}.
- Preserve the user's explicitly stated time.
- Do not invent a specific location unless the user stated it.

Commitment format:
{{
  "text": "...",
  "person": "...",
  "deadline": "..."
}}

Planned action format:
{{
  "text": "...",
  "completed": false
}}

Rules:
- Do not invent facts.
- If the exact date/year is not known, use the current date context only when
  it can be safely inferred from words like "tomorrow".
- Do not create fake times.
- Preserve important user context in notes.
- A promise such as "I promised my supervisor I would send the report"
  is a commitment.
- An explicit task such as "I added Send the report to my tasks"
  is a planned action.
- Locations mentioned by the user should go into locations.
- Return JSON only.

Current date: {today.isoformat()}

User text:
{text}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You extract structured context for BlindSpot. Return JSON only.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)

    return WorldModel(
        events=[
            CalendarEvent(**event)
            for event in data.get("events", [])
        ],
        commitments=[
            Commitment(**commitment)
            for commitment in data.get("commitments", [])
        ],
        planned_actions=[
            PlannedAction(**action)
            for action in data.get("planned_actions", [])
        ],
        notes=data.get("notes", []),
        locations=data.get("locations", []),
    )
