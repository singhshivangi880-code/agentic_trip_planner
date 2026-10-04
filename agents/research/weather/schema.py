from pydantic import BaseModel

class WeatherResult(BaseModel):
    typical_climate: str
    expected_temperature_c: float
    expected_rain: bool
    weather_sensitive_activity_flag: bool
    confidence: float
