from datetime import datetime
from agents.itinerary.schema import Itinerary

class ValidationResult:
    def __init__(self):
        self.is_valid = True
        self.errors = []
        self.warnings = []

def parse_time(time_str: str) -> int:
    """Convert HH:MM to minutes since midnight for easy comparison."""
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def validate_itinerary(itinerary: Itinerary, trip_start_date: str, trip_end_date: str) -> ValidationResult:
    result = ValidationResult()
    seen_activities = set()

    try:
        start_dt = datetime.strptime(trip_start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(trip_end_date, "%Y-%m-%d").date()
    except ValueError:
        result.errors.append("Trip bounds have invalid date format.")
        result.is_valid = False
        return result

    for day in itinerary.days:
        # 23.6 Date validator
        try:
            day_dt = datetime.strptime(day.date, "%Y-%m-%d").date()
            if not (start_dt <= day_dt <= end_dt):
                result.errors.append(f"Day {day.day_index} date {day.date} is outside trip bounds {trip_start_date} to {trip_end_date}.")
                result.is_valid = False
        except ValueError:
            result.errors.append(f"Invalid date format: {day.date}")
            result.is_valid = False

        prev_end = -1
        
        for item in day.items:
            # 23.1 Time validator
            try:
                start_m = parse_time(item.start_time)
                end_m = parse_time(item.end_time)
            except ValueError:
                result.errors.append(f"Invalid time format in '{item.title}': {item.start_time} - {item.end_time}")
                result.is_valid = False
                continue

            if start_m >= end_m:
                result.errors.append(f"Activity '{item.title}' has start time >= end time.")
                result.is_valid = False

            if start_m < prev_end:
                result.errors.append(f"Activity '{item.title}' overlaps with previous activity on day {day.day_index}.")
                result.is_valid = False
            
            prev_end = max(prev_end, end_m)

            # 23.5 Duplicate validator
            if item.item_type not in ["Transit", "Meal"]:
                if item.title in seen_activities:
                    result.warnings.append(f"Possible duplicate activity detected: '{item.title}'.")
                seen_activities.add(item.title)
                
            # 23.2, 23.3, 23.4 (Opening hours, Route, Bookings) 
            # Note: For ponytail, we leave these out until explicit strict data constraints are provided.
            # Right now, we rely on Gemini to have respected the transit times.
            
    return result
