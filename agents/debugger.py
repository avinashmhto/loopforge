from core.llm import call_llm
from core.json_utils import extract_json


def debugger_agent(user_goal: str, current_files: str, test_result: dict) -> dict:
    prompt = f"""
You are the Debugger Agent in LoopForge.

Your job is to fix failing Python/FastAPI projects.

User goal:
{user_goal}

Current project files:
{current_files}

Test command:
{test_result["command"]}

STDOUT:
{test_result["stdout"]}

STDERR:
{test_result["stderr"]}

Return ONLY valid JSON.

Format:
{{
  "summary": "short explanation of what you fixed",
  "files": [
    {{
      "path": "generated_apps/multi_agent_app/app/main.py",
      "content": "updated app code"
    }},
    {{
      "path": "generated_apps/multi_agent_app/tests/test_main.py",
      "content": "updated test code"
    }},
    {{
      "path": "generated_apps/multi_agent_app/requirements.txt",
      "content": "fastapi\\nuvicorn\\npytest\\nhttpx"
    }}
  ]
}}

Rules:
- Fix the failing tests.
- Keep paths exactly under generated_apps/multi_agent_app.
- Do not explain outside JSON.
"""

    raw = call_llm(
        "You are a Debugger Agent. You analyze failing tests and return corrected project files.",
        prompt,
    )

    return extract_json(raw)