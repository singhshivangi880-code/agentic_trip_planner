WEATHER_RESEARCH_PROMPT = """
You are an expert travel researcher. Extract a weather forecast and typical climate details for the destination.
LOCATION: {context}
RESEARCH MATERIALS:
===START EXTERNAL===
{research_context}
===END EXTERNAL===
"""
