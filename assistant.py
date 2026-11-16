
import os
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Error: Groq API key not found!")
    exit()

client = Groq(api_key=api_key)

print("\n====================================")
print("       AI STUDENT STUDY ASSISTANT")
print("====================================")
print("Ask anything about AI, ML, DSA and Programming.")
print("Type 'exit' to close the assistant.")
print("====================================")


def get_response(question):
    messages = [
        {
            "role": "system",
            "content": """
You are an AI Student Study Assistant.

Help students with:
1. Artificial Intelligence
2. Machine Learning
3. Data Structures and Algorithms
4. Programming
5. Computer Science subjects

Explain concepts in simple and beginner-friendly language.
Give examples wherever useful.
Provide step-by-step explanations when needed.
For programming questions, provide correct code.
For DSA questions, explain the approach and time complexity.
Keep answers relevant to the student's question.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
               model="openai/gpt-oss-120b",
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )

            return response.choices[0].message.content

        except Exception as e:
            error = str(e)

            if any(code in error for code in ["429", "500", "502", "503", "504"]):
                if attempt < 2:
                    print("Server busy. Retrying...")
                    time.sleep(3)
                else:
                    return "AI service is temporarily unavailable. Please try again later."

            else:
                return f"Something went wrong: {error}"


while True:
    try:
        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("\nAssistant: Goodbye! Happy Learning!")
            break

        if not question:
            print("Assistant: Please enter a question.")
            continue

        print("\nAssistant: Thinking...\n")

        answer = get_response(question)

        print("Assistant:", answer)
        print("\n" + "-" * 50)

    except KeyboardInterrupt:
        print("\nAssistant: Goodbye! Happy Learning!")
        break
