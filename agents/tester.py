import json
from core.llm import call_llm
from core.json_utils import extract_json


def tester_agent(
    user_goal: str,
    plan: dict,
    architecture: dict,
    code_project: dict,
) -> dict:
    prompt = f"""
You are the Test Agent in LoopForge.

Generate pytest tests for this application.

User goal:
{user_goal}

Plan:
{json.dumps(plan, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Implementation summary:
{code_project.get("summary", "")}

Return ONLY valid JSON.

Format:
{{
  "summary": "short testing summary",
  "files": [
    {{
      "path": "generated_apps/multi_agent_app/tests/test_main.py",
      "content": "pytest test code"
    }}
  ]
}}

Rules:
- Use fastapi.testclient.TestClient.
- Import app using: from app.main import app
- Cover create, list, get, update, delete where applicable.
- Include negative tests for missing resources.
"""

    raw = call_llm(
        "You are a Test Agent. You generate pytest test suites for FastAPI apps.",
        prompt,
    )

    return extract_json(raw)