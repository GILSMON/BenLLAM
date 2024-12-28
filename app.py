from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv
import re

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Make sure it's set in the .env file.")

# Define the API endpoint and headers
API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Replace with the actual endpoint
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Define your payload method
def payload_method(question):
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": question}]
    }
    return payload

def clean_response(response):
    """
    Clean the chatbot's response by removing escape characters and ensuring proper formatting.
    
    Args:
        response (str): The raw response from the chatbot.
    
    Returns:
        str: A cleaned version of the response.
    """
    # Remove non-printable characters (like control characters)
    response = ''.join(ch for ch in response if ch.isprintable())

    # Replace multiple spaces with a single space
    response = re.sub(r'\s+', ' ', response)

    # Ensure proper line breaks and indentation (if required)
    response = response.strip()  # Strip leading/trailing whitespace

    return response

# Define the query method
def queryQ(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        

        if response.status_code == 200:
            response_json = response.json()
            content = response_json['choices'][0]['message']['content']
            content = clean_response(content)
            return content
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return str(e)
    




# Initialize Flask app
app = Flask(__name__)

# Serve the main chat page
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    question = data.get("message")
    if question:
        payload = payload_method(question)
        response = queryQ(payload)
        return jsonify({"response": response})
    return jsonify({"response": "No message received."}), 400

# Run the app
if __name__ == "__main__":
    app.run(debug=True)