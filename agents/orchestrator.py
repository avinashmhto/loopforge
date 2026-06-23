import os
from dotenv import load_dotenv

from core.state import AgentState
from agents.planner import planner_agent
from agents.worker import worker_agent
from agents.reviewer import reviewer_agent

load_dotenv()

MAX_LOOPS = int(os.getenv("MAX_LOOPS", "5"))
PASSING_SCORE = int(os.getenv("PASSING_SCORE", "90"))


def run_loop(goal: str):
    state = AgentState(goal=goal)

    for i in range(1, MAX_LOOPS + 1):
        state.iteration = i

        print("\n==============================")
        print(f"LoopForge Iteration {i}")
        print("==============================")

        state = planner_agent(state)
        state = worker_agent(state)
        state = reviewer_agent(state)

        state.history.append(
            {
                "iteration": i,
                "plan": state.plan,
                "work_output": state.work_output,
                "review": state.review,
            }
        )

        print("\nReviewer:", state.review)

        missing_items = state.review.get("missing_items", [])
        score = state.review.get("score", 0)
        solved = state.review.get("solved", False)

        if solved is True and score >= PASSING_SCORE and len(missing_items) == 0:
            print("\n✅ Goal solved. Stopping loop.")
            break

        print("\n🔁 Not fully solved yet. Continuing loop...")

    return state