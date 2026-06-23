import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")


def call_llm(system_role: str, user_prompt: str) -> str:
    print(f"\n🔵 Calling LLM: {system_role}")

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": system_role,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    )

    print(f"✅ Completed: {system_role}")

    return response.output_text