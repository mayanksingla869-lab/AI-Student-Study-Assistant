
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not client:
        return jsonify({"error": "Groq API key not found. Check your .env file."}), 500

    data = request.get_json(silent=True) or {}
    question = data.get("message", "").strip()
    history = data.get("history", [])

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    messages = [
        {
            "role": "system",
            "content": "You are an AI Student Study Assistant. Help students with AI, ML, DSA, programming and computer science. Explain concepts in simple language with examples."
        }
    ]

    for item in history[-10:]:
        role = item.get("role")
        content = item.get("content", "")
        if role in ("user", "assistant") and isinstance(content, str):
            messages.append({"role": role, "content": content[:4000]})

    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer or "No response generated."})

    except Exception as e:
        print("Groq API error:", str(e))
        return jsonify({"error": "Unable to generate a response. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)
