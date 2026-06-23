from agents.orchestrator import run_loop
from agents.software_engineer import auto_software_engineer


if __name__ == "__main__":
    print("Choose mode:")
    print("1. Agent Loop")
    print("2. Auto Software Engineer")

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

    else:
        goal = input("Enter your goal for LoopForge: ")
        result = run_loop(goal)

        print("\n\nFINAL OUTPUT")
        print("Status:", "Solved" if result.review.get("solved") else "Not fully solved")
        print("Iterations:", result.iteration)
        print("\nAnswer:\n")
        print(result.work_output)