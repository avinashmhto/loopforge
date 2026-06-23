from tools.file_tool import write_file


def generate_report(
    output_path: str,
    user_goal: str,
    status: str,
    attempts: int,
    summary: str,
    test_stdout: str,
):
    report = f"""
# LoopForge Execution Report

## User Goal
{user_goal}

## Status
{status}

## Attempts
{attempts}

## AI Summary
{summary}

## Test Output

{test_stdout}

Generated automatically by LoopForge.
"""

    write_file(output_path, report)