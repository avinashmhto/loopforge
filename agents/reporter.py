from tools.report_tool import generate_report


APP_DIR = "generated_apps/multi_agent_app"


def reporter_agent(
    user_goal: str,
    status: str,
    attempts: int,
    summary: str,
    test_result: dict,
):
    output_path = f"{APP_DIR}/loopforge_report.md"

    generate_report(
        output_path=output_path,
        user_goal=user_goal,
        status=status,
        attempts=attempts,
        summary=summary,
        test_stdout=test_result["stdout"],
    )

    return output_path