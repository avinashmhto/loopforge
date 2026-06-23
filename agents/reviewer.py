import json
from core.llm import call_llm
from core.json_utils import extract_json


def reviewer_agent(state):
    prompt = f"""
Goal:
{state.goal}

Worker output:
{state.work_output}

Review the output.

Return ONLY valid JSON in this format:

{{
  "solved": true,
  "score": 85,
  "feedback": "short feedback",
  "missing_items": []
}}
"""

    raw_review = call_llm(
        "You are a Reviewer Agent. Your job is to judge if the task is solved.",
        prompt,
    )

    try:
        state.review = json.loads(raw_review)
    except Exception:
        state.review = {
            "solved": False,
            "score": 0,
            "feedback": "Reviewer returned invalid JSON.",
            "missing_items": ["Fix reviewer JSON format"],
        }

    return state


def engineering_reviewer_agent(user_goal: str, test_result: dict) -> dict:
    prompt = f"""
You are the Reviewer Agent in LoopForge.

Review whether the generated project satisfies the user goal.

User goal:
{user_goal}

Test result:
{json.dumps(test_result, indent=2)}

Return ONLY valid JSON.

Format:
{{
  "approved": true,
  "score": 95,
  "summary": "short review summary",
  "missing_items": []
}}

Rules:
- Approve only if tests passed.
- If returncode is not 0, approved must be false.
"""

    raw = call_llm(
        "You are a Reviewer Agent. You approve or reject final software output.",
        prompt,
    )

    return extract_json(raw)