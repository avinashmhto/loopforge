from tools.shell_tool import run_command


APP_DIR = "generated_apps/multi_agent_app"


def executor_agent() -> dict:
    return run_command(f"cd {APP_DIR} && python -m pytest")