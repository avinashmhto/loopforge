from core.llm import call_llm


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