from orchestrator.workflow_engine import run_workflow_engine


if __name__ == "__main__":
    print("Choose mode:")
    print("1. True Multi-Agent Engineer")

    choice = input("Enter choice: ")

    if choice == "1":
        goal = input("What should LoopForge build? ")

        result = run_workflow_engine(goal)

        print("\n==============================")
        print("TRUE MULTI-AGENT ENGINEER RESULT")
        print("==============================")
        print("Status:", result["status"])
        print("Attempts:", result["attempts"])
        print("Summary:", result["summary"])

        if result["status"] == "passed":
            print("\n✅ Multi-agent workflow completed successfully.")
        else:
            print("\n❌ Multi-agent workflow failed after max attempts.")