import json
from core.llm import call_llm


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