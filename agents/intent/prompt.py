INTENT_EXTRACTION_PROMPT = """
You are an expert travel agent. Your task is to extract structured intent from the user's trip request and their profile.
Do not invent or assume information. If critical information like destination or duration is missing, add it to 'missing_information'.

User Request:
{request}

User Profile:
{profile}
"""
