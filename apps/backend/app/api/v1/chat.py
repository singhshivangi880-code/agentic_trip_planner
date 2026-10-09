import os
import json
from typing import Optional, List
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.security import rate_limit

router = APIRouter(prefix="/agent", tags=["agent-chat"])

class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class AgentChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []
    current_trip: Optional[dict] = None

class LocationValidation(BaseModel):
    is_valid: bool = True
    flags: List[str] = []
    suggestions: List[str] = []
    normalized_origin: Optional[str] = None
    normalized_destination: Optional[str] = None

class ExtractedTripData(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    duration_days: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[str] = None
    pace: Optional[str] = None
    interests: List[str] = []

class AgentChatResponse(BaseModel):
    reply: str
    validation: Optional[LocationValidation] = None
    extracted_trip: Optional[ExtractedTripData] = None
    show_embedded_card: bool = False
    suggested_replies: List[str] = []

AGENTIC_CHAT_SYSTEM_PROMPT = """
You are an expert, thoughtful, and highly cultured AI Travel Co-Pilot and Trip Planner.
Your role is to converse naturally with travellers, understand their travel desires, and construct authentic itineraries for ANY destination worldwide (United States, Europe, Asia, Americas, Africa, Oceania, etc.).

CRITICAL VALIDATION & EXTRACTION RULES:
1. DESTINATION & ORIGIN EXTRACTION:
   - Carefully extract the DESTINATION that the user wants to visit from their message (e.g. "5 days in Unites States" -> destination is "United States"). NEVER default or substitute another country like Japan unless the user explicitly asked for Japan.
   - Detect and correct typos gracefully (e.g. "Unites States" -> "United States", "pube" -> "Pune" or "Phuket", "parsi" -> "Paris", "tokio" -> "Tokyo").
   - If origin/departure is not specified by the user, keep extracted_origin as null / None. Do NOT assume or default to Pune or any other city unless the user stated it or it is already in the working trip state!
   - In your reply, if the departure origin is unknown, ask them: "Where will you be departing from?"
   - If destination is a broad country (e.g. "United States", "Japan", "Italy"), acknowledge it enthusiastically, suggest iconic focus regions (e.g. for US: New York & East Coast vs California & West Coast; for Japan: Tokyo & Kyoto), and ask what style they prefer.

2. EMBEDDED CONFIRMATION CARD:
   - When a valid destination is identified, set show_embedded_card = True, and populate extracted_trip with the actual extracted destination and duration.
   - If origin is known, include it; if unknown, leave it empty for the user to fill in the card or chat.

3. CONVERSATIONAL TONE:
   - Editorial, warm, personal, and helpful.
   - Reference their specific destination and ideas directly. Never give generic boilerplate.
"""

class LLMStructuredOutput(BaseModel):
    reply: str = Field(description="Conversational response to the traveller.")
    validation_is_valid: bool = Field(default=True, description="False if origin or destination has typos or errors.")
    validation_flags: List[str] = Field(default_factory=list, description="List of warning messages regarding locations.")
    validation_suggestions: List[str] = Field(default_factory=list, description="Suggested city/airport corrections.")
    normalized_origin: Optional[str] = Field(default=None, description="Cleaned, capitalized origin name if provided, else None.")
    normalized_destination: Optional[str] = Field(default=None, description="Cleaned, capitalized destination name if provided, else None.")
    extracted_origin: Optional[str] = None
    extracted_destination: Optional[str] = None
    extracted_duration_days: Optional[int] = None
    extracted_budget: Optional[str] = None
    extracted_pace: Optional[str] = None
    extracted_interests: List[str] = Field(default_factory=list)
    show_embedded_card: bool = False
    suggested_replies: List[str] = Field(default_factory=list, description="2-4 quick prompt chips for the user.")


@router.post("/chat", response_model=AgentChatResponse, dependencies=[rate_limit(times=60, seconds=60)])
async def chat_with_agent(req: AgentChatRequest):
    """
    Agentic conversational endpoint for trip ideation, typo detection, and location validation.
    """
    user_msg = req.message.strip()
    history_text = "\n".join([f"{m.role}: {m.content}" for m in req.history[-6:]])
    current_trip_json = json.dumps(req.current_trip or {})

    prompt = f"""
{AGENTIC_CHAT_SYSTEM_PROMPT}

Recent Conversation History:
{history_text}

Current Working Trip State:
{current_trip_json}

Latest User Message:
"{user_msg}"

Evaluate the message, perform agentic location verification, extract parameters, and respond with JSON matching schema.
"""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        for model_name in ["gemini-flash-latest", "gemini-3.8-flash", "gemini-2.5-flash-lite"]:
            try:
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=gemini_key)
                res = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=LLMStructuredOutput,
                        temperature=0.3
                    )
                )
                if res and res.text:
                    parsed = LLMStructuredOutput.model_validate_json(res.text)
                    return AgentChatResponse(
                        reply=parsed.reply,
                        validation=LocationValidation(
                            is_valid=parsed.validation_is_valid,
                            flags=parsed.validation_flags,
                            suggestions=parsed.validation_suggestions,
                            normalized_origin=parsed.normalized_origin,
                            normalized_destination=parsed.normalized_destination
                        ),
                        extracted_trip=ExtractedTripData(
                            origin=parsed.extracted_origin or parsed.normalized_origin or (req.current_trip or {}).get("origin"),
                            destination=parsed.extracted_destination or parsed.normalized_destination or (req.current_trip or {}).get("destination"),
                            duration_days=parsed.extracted_duration_days or (req.current_trip or {}).get("duration_days"),
                            budget=parsed.extracted_budget or (req.current_trip or {}).get("budget"),
                            pace=parsed.extracted_pace or (req.current_trip or {}).get("pace"),
                            interests=parsed.extracted_interests or (req.current_trip or {}).get("interests", [])
                        ),
                        show_embedded_card=parsed.show_embedded_card or bool(parsed.extracted_destination or parsed.normalized_destination),
                        suggested_replies=parsed.suggested_replies
                    )
            except Exception as e:
                continue

    # High-intelligence local agentic reasoning fallback
    return agentic_fallback_reasoning(user_msg, req.current_trip, req.history)


def agentic_fallback_reasoning(user_msg: str, current_trip: Optional[dict], history: List[ChatMessage]) -> AgentChatResponse:
    """Agentic heuristic reasoning engine when external LLM API is unavailable."""
    import re
    msg_lower = user_msg.lower()
    
    # 1. Typo detection dictionary
    typos = {
        "pube": ("Pune, India", ["Pune", "Phuket"]),
        "puna": ("Pune, India", ["Pune"]),
        "unites states": ("United States", ["United States", "New York", "California"]),
        "untied states": ("United States", ["United States", "New York", "California"]),
        "amreica": ("America / United States", ["United States", "New York"]),
        "delh": ("Delhi, India", ["New Delhi"]),
        "mubai": ("Mumbai, India", ["Mumbai"]),
        "bombay": ("Mumbai, India", ["Mumbai"]),
        "banglore": ("Bengaluru, India", ["Bengaluru"]),
        "tokio": ("Tokyo, Japan", ["Tokyo"]),
        "japn": ("Japan", ["Tokyo, Japan", "Kyoto, Japan"]),
        "parsi": ("Paris, France", ["Paris"])
    }

    found_typo = None
    for typo, (correction, suggestions) in typos.items():
        if typo in msg_lower:
            found_typo = (typo, correction, suggestions)
            break

    # 2. Extract Destination dynamically
    found_dest = None
    
    # Check known destinations map
    known_destinations = {
        "unites states": "United States",
        "united states": "United States",
        "usa": "United States",
        "us": "United States",
        "america": "United States",
        "new york": "New York, USA",
        "california": "California, USA",
        "japan": "Japan",
        "tokyo": "Tokyo, Japan",
        "kyoto": "Kyoto, Japan",
        "osaka": "Osaka, Japan",
        "paris": "Paris, France",
        "france": "France",
        "italy": "Italy",
        "rome": "Rome, Italy",
        "florence": "Florence, Italy",
        "switzerland": "Switzerland",
        "zurich": "Zurich, Switzerland",
        "bali": "Bali, Indonesia",
        "indonesia": "Indonesia",
        "united kingdom": "United Kingdom",
        "uk": "United Kingdom",
        "london": "London, UK",
        "singapore": "Singapore",
        "dubai": "Dubai, UAE",
        "australia": "Australia",
        "sydney": "Sydney, Australia",
        "iceland": "Iceland",
        "spain": "Spain",
        "barcelona": "Barcelona, Spain",
        "germany": "Germany",
        "berlin": "Berlin, Germany",
        "thailand": "Thailand",
        "bangkok": "Bangkok, Thailand"
    }

    for k, d_val in known_destinations.items():
        pattern = r'\b' + re.escape(k) + r'\b'
        if re.search(pattern, msg_lower):
            found_dest = d_val
            break

    # If still not found, try dynamic regex extraction: "in/to/visit/trip to <Place>"
    if not found_dest:
        dest_match = re.search(r'(?:in|to|visit|exploring|trip to)\s+([a-zA-Z\s]{3,25})', user_msg, re.IGNORECASE)
        if dest_match:
            candidate = dest_match.group(1).strip()
            # Clean candidate of trailing words
            candidate = re.sub(r'\s+(?:for|from|with|during|in|and)\b.*$', '', candidate, flags=re.IGNORECASE).strip()
            if candidate and candidate.lower() not in ["a", "an", "the", "my", "our", "some"]:
                found_dest = candidate.title()

    # 3. Extract Origin dynamically
    found_origin = None
    orig_match = re.search(r'(?:from|departing from|leaving from|flying from)\s+([a-zA-Z\s]{3,25})', user_msg, re.IGNORECASE)
    if orig_match:
        candidate_orig = orig_match.group(1).strip()
        candidate_orig = re.sub(r'\s+(?:to|for|with|during|and)\b.*$', '', candidate_orig, flags=re.IGNORECASE).strip()
        if candidate_orig:
            found_origin = candidate_orig.title()

    # Known origins check if regex missed
    if not found_origin:
        known_origins = ["mumbai", "delhi", "pune", "bengaluru", "hyderabad", "chennai", "kolkata", "london", "new york", "san francisco", "chicago", "singapore", "dubai"]
        for o in known_origins:
            if re.search(r'\b' + re.escape(o) + r'\b', msg_lower):
                found_origin = o.title()
                break

    # 4. Extract Days
    duration = 7
    dur_match = re.search(r'(\d+)\s*(days?|weeks?|d\b)', msg_lower)
    if dur_match:
        num = int(dur_match.group(1))
        unit = dur_match.group(2)
        duration = num * 7 if "week" in unit else num

    # 5. Extract Interests
    interests = []
    for tag in ["food", "ramen", "culture", "anime", "history", "nature", "shopping", "luxury", "budget", "museum", "wine", "beach", "nightlife", "hiking"]:
        if tag in msg_lower:
            interests.append(tag.capitalize())

    # 6. Handle Typo Flag
    if found_typo:
        bad_word, fix, sug = found_typo
        return AgentChatResponse(
            reply=f"I noticed **'{bad_word}'** looks like a typo for a location. Did you mean **{fix}**? Let me know so I can coordinate flight paths and transit options accurately.",
            validation=LocationValidation(
                is_valid=False,
                flags=[f"'{bad_word}' was flagged as an unrecognized location."],
                suggestions=sug,
                normalized_destination=fix if "united" in fix.lower() or "japan" in fix.lower() or "paris" in fix.lower() else None,
                normalized_origin=sug[0] if "pune" in bad_word else None
            ),
            extracted_trip=ExtractedTripData(
                origin=found_origin or (current_trip or {}).get("origin"),
                destination=fix if "united" in fix.lower() or "japan" in fix.lower() or "paris" in fix.lower() else found_dest,
                duration_days=duration,
                interests=interests
            ),
            show_embedded_card=bool(found_dest or fix),
            suggested_replies=[f"Yes, {sug[0]}", f"I mean {sug[1]}" if len(sug) > 1 else "Different City", "Adjust details"]
        )

    # 7. Identical Origin & Destination Check
    if found_origin and found_dest and found_origin.lower() == found_dest.lower():
        return AgentChatResponse(
            reply=f"Your departure and destination are both set to **{found_origin}**. Please choose a different destination for your journey!",
            validation=LocationValidation(
                is_valid=False,
                flags=["Origin and destination cannot be identical."]
            ),
            show_embedded_card=False,
            suggested_replies=["Travel to United States", "Travel to Japan", "Travel to Paris"]
        )

    # Determine final values
    final_dest = found_dest or (current_trip or {}).get("destination")
    final_orig = found_origin or (current_trip or {}).get("origin")

    # If no destination could be determined at all
    if not final_dest:
        return AgentChatResponse(
            reply="I'd love to help craft your ideal getaway! Which destination are you dreaming of exploring (for example: **United States**, **Japan**, **France**, or **Italy**)?",
            validation=LocationValidation(is_valid=True),
            show_embedded_card=False,
            suggested_replies=["5 days in United States", "14 days in Japan", "7 days in Paris", "10 days in Italy"]
        )

    # Construct intelligent conversational reply
    reply_parts = [f"Wonderful idea! Planning a **{duration}-day journey to {final_dest}**"]
    if final_orig:
        reply_parts.append(f"departing from **{final_orig}**.")
    else:
        reply_parts.append(". Where will you be flying or departing from?")

    if "united states" in final_dest.lower() or "usa" in final_dest.lower() or "america" in final_dest.lower():
        reply_parts.append(" For a 5-day journey in the United States, I recommend focusing on either **New York City** (iconic Manhattan, Central Park, Broadway & world-class dining) or California's coast.")
    elif "japan" in final_dest.lower():
        reply_parts.append(" In Japan, I recommend our balanced route: **Tokyo** for neon skylines and Tsukiji sashimi, **Kyoto** for shrines, and **Osaka** for street food.")
    elif "paris" in final_dest.lower() or "france" in final_dest.lower():
        reply_parts.append(" In France, we will balance iconic art at the Louvre with historic bistros and golden hour river cruises.")
    else:
        reply_parts.append(f" I have mapped out optimal regional pacing and curated highlights for {duration} days.")

    reply_text = "".join(reply_parts)

    return AgentChatResponse(
        reply=reply_text,
        validation=LocationValidation(
            is_valid=True,
            normalized_origin=final_orig,
            normalized_destination=final_dest
        ),
        extracted_trip=ExtractedTripData(
            origin=final_orig,
            destination=final_dest,
            duration_days=duration,
            pace="balanced",
            budget="moderate",
            interests=interests if interests else ["Highlights", "Culture"]
        ),
        show_embedded_card=True,
        suggested_replies=[
            "Looks perfect, generate itinerary!",
            "Focus on New York City" if "united states" in final_dest.lower() else "Focus on city center",
            "Make it relaxed pace",
            "Change departure city"
        ]
    )
