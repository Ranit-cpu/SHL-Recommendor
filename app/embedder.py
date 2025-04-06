import os
import openai
import requests

# Load API keys
GEMINI_API_KEY = "AIzaSyCJ2OSEgSjqq6OandlmUwRpZRwuOJiBAuU"
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

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
