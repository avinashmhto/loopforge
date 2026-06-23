from core.llm import call_llm


def worker_agent(state):
    prompt = f"""
Goal:
{state.goal}

Plan:
{state.plan}

Previous history:
{state.history}

Execute the plan and produce the best possible answer.
"""

    state.work_output = call_llm(
        "You are a Worker Agent. Your job is to execute the planner's instructions.",
        prompt,
    )

    return state