import json
import os

from core.llm import call_llm
from tools.file_tool import write_file, read_file
from tools.shell_tool import run_command
from tools.report_tool import generate_report


APP_DIR = "generated_apps/dynamic_app"
MAX_FIX_LOOPS = 3


def _extract_json(raw: str) -> dict:
    raw = raw.strip()

    if raw.startswith("```json"):
        raw = raw.replace("```json", "").replace("```", "").strip()
    elif raw.startswith("```"):
        raw = raw.replace("```", "").strip()

    return json.loads(raw)


def generate_app_files(user_goal: str) -> dict:
    prompt = f"""
You are an Auto Software Engineer.

Create a small FastAPI application for this request:

{user_goal}

Return ONLY valid JSON.

Format:
{{
  "summary": "short summary",
  "files": [
    {{
      "path": "generated_apps/dynamic_app/app/main.py",
      "content": "file content here"
    }},
    {{
      "path": "generated_apps/dynamic_app/tests/test_main.py",
      "content": "file content here"
    }},
    {{
      "path": "generated_apps/dynamic_app/requirements.txt",
      "content": "fastapi\\nuvicorn\\npytest\\nhttpx"
    }}
  ]
}}

Rules:
- Use FastAPI.
- Include pytest tests.
- Use in-memory data only.
- Keep it simple.
- All imports must work.
- Tests should run with: python -m pytest
"""

    raw = call_llm(
        "You generate complete working software projects as JSON files.",
        prompt,
    )

    return _extract_json(raw)


def write_generated_files(project: dict):
    for file in project["files"]:
        write_file(file["path"], file["content"])


def run_tests():
    return run_command(f"cd {APP_DIR} && python -m pytest")


def collect_project_files() -> str:
    files_to_read = [
        f"{APP_DIR}/app/main.py",
        f"{APP_DIR}/tests/test_main.py",
        f"{APP_DIR}/requirements.txt",
    ]

    content = ""

    for path in files_to_read:
        if os.path.exists(path):
            content += f"\n\n--- {path} ---\n"
            content += read_file(path)

    return content


def fix_project(user_goal: str, test_result: dict) -> dict:
    current_files = collect_project_files()

    prompt = f"""
You are a debugging software engineer.

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

Return ONLY valid JSON with updated files.

Format:
{{
  "summary": "what you fixed",
  "files": [
    {{
      "path": "generated_apps/dynamic_app/app/main.py",
      "content": "updated file content"
    }},
    {{
      "path": "generated_apps/dynamic_app/tests/test_main.py",
      "content": "updated file content"
    }},
    {{
      "path": "generated_apps/dynamic_app/requirements.txt",
      "content": "updated requirements"
    }}
  ]
}}

Rules:
- Fix the failing tests.
- Do not explain outside JSON.
- Keep paths exactly under generated_apps/dynamic_app.
"""

    raw = call_llm(
        "You fix failing Python FastAPI projects and return corrected files as JSON.",
        prompt,
    )

    return _extract_json(raw)


def inject_demo_bug():
    main_path = f"{APP_DIR}/app/main.py"
    content = read_file(main_path)

    if "@app.delete" in content:
        broken_content = content.split("@app.delete")[0]
        broken_content += "\n\n# DEMO BUG: delete endpoint removed intentionally\n"
        write_file(main_path, broken_content)
        print("🐞 Demo bug injected: DELETE endpoint removed.")
    else:
        print("⚠️ Demo bug not injected because DELETE endpoint was not found.")


def auto_software_engineer(user_goal: str):
    print("\n🧠 Generating application...")
    project = generate_app_files(user_goal)
    write_generated_files(project)

    initial_summary = project.get("summary", "")
    fix_summaries = []

    print("\n🐞 Injecting demo bug so LoopForge can prove auto-fix...")
    inject_demo_bug()

    print("\n📁 Files generated.")
    print("Summary:", initial_summary)

    for attempt in range(1, MAX_FIX_LOOPS + 1):
        print(f"\n🧪 Running tests - Attempt {attempt}")
        test_result = run_tests()

        print("\nSTDOUT:\n", test_result["stdout"])
        print("\nSTDERR:\n", test_result["stderr"])

        if test_result["returncode"] == 0:
            final_summary = project.get("summary", initial_summary)

            generate_report(
                output_path=f"{APP_DIR}/loopforge_report.md",
                user_goal=user_goal,
                status="passed",
                attempts=attempt,
                summary=final_summary,
                test_stdout=test_result["stdout"],
            )

            print(f"\n📝 Report generated: {APP_DIR}/loopforge_report.md")

            return {
                "status": "passed",
                "attempts": attempt,
                "summary": final_summary,
                "fix_summaries": fix_summaries,
                "test_result": test_result,
            }

        print("\n🔧 Tests failed. Asking LLM to fix the project...")
        project = fix_project(user_goal, test_result)

        fix_summary = project.get("summary", "")
        if fix_summary:
            fix_summaries.append(fix_summary)

        write_generated_files(project)

    final_summary = project.get("summary", initial_summary)

    generate_report(
        output_path=f"{APP_DIR}/loopforge_report.md",
        user_goal=user_goal,
        status="failed",
        attempts=MAX_FIX_LOOPS,
        summary=final_summary,
        test_stdout=test_result["stdout"],
    )

    print(f"\n📝 Report generated: {APP_DIR}/loopforge_report.md")

    return {
        "status": "failed",
        "attempts": MAX_FIX_LOOPS,
        "summary": final_summary,
        "fix_summaries": fix_summaries,
        "test_result": test_result,
    }