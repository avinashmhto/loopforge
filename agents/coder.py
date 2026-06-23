import json
from core.llm import call_llm
from core.json_utils import extract_json


def coder_agent(user_goal: str, plan: dict, architecture: dict) -> dict:
    prompt = f"""
You are the Code Agent in LoopForge.

Generate implementation files for the application.

User goal:
{user_goal}

Plan:
{json.dumps(plan, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Return ONLY valid JSON.

Format:
{{
  "summary": "short implementation summary",
  "files": [
    {{
      "path": "generated_apps/multi_agent_app/app/main.py",
      "content": "FastAPI app code"
    }},
    {{
      "path": "generated_apps/multi_agent_app/requirements.txt",
      "content": "fastapi\\nuvicorn\\npytest\\nhttpx"
    }}
  ]
}}

Rules:
- Use FastAPI.
- Use in-memory storage only.
- Include proper HTTP status codes.
- Make the app importable from app.main.
- Do not include tests here.
"""

    raw = call_llm(
        "You are a Code Agent. You write clean Python FastAPI implementation files.",
        prompt,
    )

    return extract_json(raw)