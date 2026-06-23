import json


def extract_json(raw: str) -> dict:
    raw = raw.strip()

    if raw.startswith("```json"):
        raw = raw.replace("```json", "").replace("```", "").strip()
    elif raw.startswith("```"):
        raw = raw.replace("```", "").strip()

    return json.loads(raw)