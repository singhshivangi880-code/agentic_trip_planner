import os, json
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional

class ItineraryItem(BaseModel):
    title: str
    item_type: str
    start_time: str
    end_time: str
    location: str
    description: str
    is_locked: bool = False

class DayPlan(BaseModel):
    day_index: int
    theme_or_area: str
    items: List[ItineraryItem]

class ItineraryPlan(BaseModel):
    days: List[DayPlan]

prompt = """Generate an authentic 3-day itinerary for Delhi, India.
CRITICAL: Use ONLY real, famous, authentic locations (e.g. Red Fort, Chandni Chowk, Qutub Minar, Humayun Tomb, India Gate, Akshardham, Karim's).
DO NOT use generic phrases like 'Old Quarter' or 'City Center'. Use real district names."""

client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
models = ['gemini-2.5-flash-lite', 'gemini-3.8-flash', 'gemini-flash-latest', 'gemini-3.1-flash-lite']
res = None
for m in models:
    try:
        res = client.models.generate_content(
            model=m,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=ItineraryPlan,
                temperature=0.2
            )
        )
        if res and res.text:
            print(f"Success with model {m}!")
            break
    except Exception as e:
        print(f"Model {m} failed: {e}")
        continue
data = json.loads(res.text)
print("=== GENERATED DAYS COUNT ===", len(data["days"]))
for d in data["days"]:
    print(f"Day {d['day_index']}: {d['theme_or_area']}")
    for item in d["items"]:
        print(f"  - [{item['location']}] {item['title']}: {item['description']}")
