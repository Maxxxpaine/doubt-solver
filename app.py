from flask import Flask, render_template, request
import requests

app = Flask(__name__)

TOGETHER_API_KEY = "bc386d81916cd04d8513f2806741bd33c503e224ffb7078127475022dfedc571"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"

def get_ai_response(question):
    headers = {"Authorization": f"Bearer {TOGETHER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo-128K",
        "messages": [{"role": "user", "content": question}]
    }
    response = requests.post(TOGETHER_API_URL, json=payload, headers=headers)
    return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")

@app.route("/", methods=["GET", "POST"])
def home():
    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        answer = get_ai_response(question)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
