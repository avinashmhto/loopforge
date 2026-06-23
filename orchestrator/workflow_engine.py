import os

from agents.planner import engineering_planner_agent
from agents.architect import architect_agent
from agents.coder import coder_agent
from agents.tester import tester_agent
from agents.executor import executor_agent
from agents.debugger import debugger_agent
from agents.reviewer import engineering_reviewer_agent
from agents.reporter import reporter_agent

from tools.file_tool import write_file, read_file


APP_DIR = "generated_apps/multi_agent_app"
MAX_FIX_LOOPS = 3


def write_project_files(project: dict):
    for file in project.get("files", []):
        write_file(file["path"], file["content"])


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


def inject_demo_bug():
    main_path = f"{APP_DIR}/app/main.py"

    if not os.path.exists(main_path):
        print("⚠️ Demo bug not injected because app/main.py was not found.")
        return

    content = read_file(main_path)

    # Preferred demo bug: remove DELETE endpoint if route decorator exists.
    if "@app.delete" in content:
        broken_content = content.split("@app.delete")[0]
        broken_content += "\n\n# DEMO BUG: delete endpoint removed intentionally\n"
        write_file(main_path, broken_content)
        print("🐞 Demo bug injected: DELETE endpoint removed.")
        return

    # Generic fallback: break the first delete-related function if decorator style is different.
    lines = content.splitlines()
    broken_lines = []
    skip_mode = False
    removed_anything = False

    for line in lines:
        lower_line = line.lower()

        if (
            "delete" in lower_line
            or "remove" in lower_line
            or "delet" in lower_line
        ):
            broken_lines.append("# DEMO BUG: delete/remove logic removed intentionally")
            skip_mode = True
            removed_anything = True
            continue

        if skip_mode:
            # Stop skipping when we hit another top-level function, class, or route.
            if (
                line.startswith("def ")
                or line.startswith("class ")
                or line.startswith("@app.")
            ):
                skip_mode = False
                broken_lines.append(line)
            else:
                continue
        else:
            broken_lines.append(line)

    if removed_anything:
        write_file(main_path, "\n".join(broken_lines))
        print("🐞 Demo bug injected: delete/remove logic removed generically.")
        return

    # Last fallback: break the root/health endpoint response.
    if "return" in content:
        broken_content = content.replace("return", "return_broken", 1)
        write_file(main_path, broken_content)
        print("🐞 Demo bug injected: first return statement broken.")
        return

    print("⚠️ Demo bug was not injected. No suitable target found.")


def run_workflow_engine(user_goal: str):
    print("\n🧠 Planner Agent: creating plan...")
    plan = engineering_planner_agent(user_goal)
    print("Planner:", plan.get("summary", ""))

    print("\n🏗️ Architect Agent: designing structure...")
    architecture = architect_agent(user_goal, plan)
    print("Architect:", architecture.get("summary", ""))

    print("\n💻 Code Agent: generating implementation...")
    code_project = coder_agent(user_goal, plan, architecture)
    write_project_files(code_project)
    print("Code Agent:", code_project.get("summary", ""))

    print("\n🧪 Test Agent: generating tests...")
    test_project = tester_agent(user_goal, plan, architecture, code_project)
    write_project_files(test_project)
    print("Test Agent:", test_project.get("summary", ""))

    print("\n🐞 Injecting demo bug so the Debugger Agent can prove auto-repair...")
    inject_demo_bug()

    final_summary = code_project.get("summary", "")

    for attempt in range(1, MAX_FIX_LOOPS + 1):
        print(f"\n⚙️ Executor Agent: running tests - Attempt {attempt}")
        test_result = executor_agent()

        print("\nSTDOUT:\n", test_result["stdout"])
        print("\nSTDERR:\n", test_result["stderr"])

        if test_result["returncode"] == 0:
            print("\n🔍 Reviewer Agent: reviewing final result...")
            review = engineering_reviewer_agent(user_goal, test_result)
            final_summary = review.get("summary", final_summary)

            print("\n📝 Reporter Agent: generating execution report...")
            report_path = reporter_agent(
                user_goal=user_goal,
                status="passed",
                attempts=attempt,
                summary=final_summary,
                test_result=test_result,
            )

            print(f"Report generated at: {report_path}")

            return {
                "status": "passed",
                "attempts": attempt,
                "summary": final_summary,
                "plan": plan,
                "architecture": architecture,
                "review": review,
                "test_result": test_result,
                "report_path": report_path,
            }

        print("\n🔧 Debugger Agent: analyzing failure and fixing project...")
        current_files = collect_project_files()
        fixed_project = debugger_agent(user_goal, current_files, test_result)
        write_project_files(fixed_project)

        final_summary = fixed_project.get("summary", final_summary)
        print("Debugger:", final_summary)

    print("\n📝 Reporter Agent: generating failure report...")
    report_path = reporter_agent(
        user_goal=user_goal,
        status="failed",
        attempts=MAX_FIX_LOOPS,
        summary=final_summary,
        test_result=test_result,
    )

    return {
        "status": "failed",
        "attempts": MAX_FIX_LOOPS,
        "summary": final_summary,
        "test_result": test_result,
        "report_path": report_path,
    }