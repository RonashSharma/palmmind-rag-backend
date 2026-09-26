import json
import google.generativeai as genai
from app.config import settings
from app.database import SessionLocal
from app.models import BookingRecord

genai.configure(api_key=settings.gemini_api_key)
llm = genai.GenerativeModel("gemini-1.5-flash")

BOOKING_KEYWORDS = ("book", "interview", "schedule", "appointment")

def wants_booking(query: str) -> bool:
    return any(word in query.lower() for word in BOOKING_KEYWORDS)

def extract_booking_fields(query: str) -> dict | None:
    # forces strict JSON back so we can parse it without regex guesswork
    prompt = (
        "Extract name, email, date, and time for an interview booking from this message. "
        'Reply ONLY with JSON like {"name": "", "email": "", "date": "", "time": ""}. '
        "If a field is missing, use an empty string.\n\n"
        f"Message: {query}"
    )
    response = llm.generate_content(prompt)
    try:
        cleaned = response.text.strip().strip("`").replace("json", "", 1)
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        return None

def save_booking(session_id: str, fields: dict):
    db = SessionLocal()
    db.add(BookingRecord(
        name=fields.get("name", ""), email=fields.get("email", ""),
        date=fields.get("date", ""), time=fields.get("time", ""),
        session_id=session_id,
    ))
    db.commit()
    db.close()