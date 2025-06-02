from fastapi import FastAPI, Form
import requests

app = FastAPI()

def query_model(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    # Print response for debugging
    response_json = response.json()
    print("API Response:", response_json)
    
    # Handle different response formats from Ollama API
    if "response" in response_json:
        return response_json["response"].strip()
    elif "message" in response_json:
        return response_json["message"].strip()
    else:
        # Return the full response as a string if the expected keys aren't found
        return str(response_json)

@app.post("/generate/")
def generate_learning_aids(text: str = Form(...)):
    prompts = {
        "explanation": f"Explain this in simple terms for a student:\n\n{text}",
        "quiz": f"Generate 5 quiz questions with answers from this educational content:\n\n{text}",
        "concepts": f"List the key terms or concepts mentioned in this content:\n\n{text}"
    }
    return {k: query_model(p) for k, p in prompts.items()}