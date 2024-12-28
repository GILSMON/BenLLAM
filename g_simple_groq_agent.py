import os
import requests
from dotenv import load_dotenv

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


# Define your query or payload
def payload_method(question):

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{
        "role": "user",
        "content": question
    
    }]
    }
    return payload


response =[]
def queryQ(payload):
    # Make the request
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    # Handle the response
    if response.status_code == 200:
        # Print the entire response JSON to debug
        # print("Full Response:", response.json())

    # Convert the response to JSON if it's not already a dictionary
        response_json = response.json()
        content = response_json['choices'][0]['message']['content']
        print(content)
    
    else:
        print(f"Error {response.status_code}: {response.text}")



# Repeatedly run the code
while True:
    try:
        question = input("What's on your mind! (Type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Agent Sai, Goodbye!")
            break
        payload = payload_method(question)
        queryQ(payload)
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully.")
        break
    



    





    


