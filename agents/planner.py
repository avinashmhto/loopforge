from core.llm import call_llm
from core.json_utils import extract_json


def planner_agent(state):
    prompt = f"""
Goal:
{state.goal}

Previous history:
{state.history}

Create a clear plan for the worker agent.
Do not solve the full task yourself.
Return practical steps only.
"""

    state.plan = call_llm(
        "You are a Planner Agent. Your job is to break goals into executable steps.",
        prompt,
    )

    return state


def engineering_planner_agent(user_goal: str) -> dict:
    prompt = f"""
You are the Planner Agent in LoopForge.

Break this user goal into a practical software engineering plan.

User goal:
{user_goal}

Return ONLY valid JSON.

Format:
{{
  "summary": "short plan summary",
  "steps": [
    "step 1",
    "step 2",
    "step 3"
  ]
}}
"""

    raw = call_llm(
        "You are a Planner Agent. You create execution plans for software engineering tasks.",
        prompt,
    )

    return extract_json(raw)