import os
import openai
import requests
from dotenv import load_dotenv

load_dotenv()

# Load API keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent?key={GEMINI_API_KEY}"

def rewrite_query_with_gemini(text: str):
    """Rewrite the user's query using Gemini for better semantic matching."""
    try:
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": f"Rewrite this job query to match SHL assessments: {text}"}]
            }]
        }

        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']

    except Exception as e:
        print("⚠️ Gemini API failed:", e)
        return text  # fallback

def get_embedding(text: str):
    """Get OpenAI embedding for the given (possibly rewritten) text."""
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']
