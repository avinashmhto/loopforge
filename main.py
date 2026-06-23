from agents.orchestrator import run_loop
from agents.software_engineer import auto_software_engineer
from agents.multi_agent_engineer import run_multi_agent_engineer


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Agent Loop")
    print("2. Auto Software Engineer")
    print("3. True Multi-Agent Engineer")

    choice = input("Enter choice: ")

    if choice == "2":
        goal = input("What should LoopForge build? ")

        result = auto_software_engineer(goal)

        print("\n==============================")
        print("AUTO SOFTWARE ENGINEER RESULT")
        print("==============================")
        print("Status:", result["status"])
        print("Attempts:", result["attempts"])
        print("Summary:", result["summary"])

        if result["status"] == "passed":
            print("\n✅ Application created and tests passed.")
        else:
            print("\n❌ Tests still failed after max attempts.")

    elif choice == "3":
        goal = input("What should the Multi-Agent Engineer build? ")

        result = run_multi_agent_engineer(goal)

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

    else:
        goal = input("Enter your goal for LoopForge: ")
        result = run_loop(goal)

        print("\n\nFINAL OUTPUT")
        print("Status:", "Solved" if result.review.get("solved") else "Not fully solved")
        print("Iterations:", result.iteration)
        print("\nAnswer:\n")
        print(result.work_output)