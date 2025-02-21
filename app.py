from flask import Flask, render_template, request, session
from flask import redirect, url_for
import requests
import re

app = Flask(__name__)
app.secret_key = "aaab86fa3608aa506d7c148f4f33cc96"  # Required for session management

TOGETHER_API_KEY = "bc386d81916cd04d8513f2806741bd33c503e224ffb7078127475022dfedc571"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

# Function to format AI response
def format_answer(answer):
    answer = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', answer)
    answer = re.sub(r'\*(.*?)\*', r'<i>\1</i>', answer)
    answer = answer.replace('\n', '<br>')
    return answer

# Function to get AI response while keeping history
def get_ai_response(history):
    headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "mistralai/Mistral-7B-Instruct-v0.1", "messages": history}
    
    response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")

@app.route("/", methods=["GET", "POST"])
def home():
    if "history" not in session:
        session["history"] = []  # Initialize empty history

    if request.method == "POST":
        user_question = request.form.get("question")
        session["history"].append({"role": "user", "content": user_question})  # Store user question

        raw_answer = get_ai_response(session["history"])  # Send full history
        formatted_answer = format_answer(raw_answer)

        session["history"].append({"role": "assistant", "content": formatted_answer})  # Store AI response
        session.modified = True  # Save session changes

    return render_template("index.html", history=session["history"])

@app.route("/clear")
def clear_chat():
    session.pop("history", None)  # Clear chat history
    return redirect(url_for("home"))  # Redirect to home page

if __name__ == "__main__":
    app.run(debug=True)
