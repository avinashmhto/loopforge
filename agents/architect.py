import json
from core.llm import call_llm
from core.json_utils import extract_json


def architect_agent(user_goal: str, plan: dict) -> dict:
    prompt = f"""
You are the Architect Agent in LoopForge.

Design the project structure for this goal.

User goal:
{user_goal}

Planner output:
{json.dumps(plan, indent=2)}

Return ONLY valid JSON.

Format:
{{
  "summary": "short architecture summary",
  "project_type": "FastAPI",
  "files": [
    "generated_apps/multi_agent_app/app/main.py",
    "generated_apps/multi_agent_app/tests/test_main.py",
    "generated_apps/multi_agent_app/requirements.txt"
  ]
}}
"""

    raw = call_llm(
        "You are an Architect Agent. You design clean project structures.",
        prompt,
    )

    return extract_json(raw)