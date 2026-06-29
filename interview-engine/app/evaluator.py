import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_answer(question: str, user_answer: str):
    prompt = f"""
You are evaluating a mock interview answer.

Question: {question}
Candidate answer: {user_answer}

Return ONLY valid JSON in this exact format, no extra text:
{{
  "score": <integer 0-10>,
  "strengths": "<what was good>",
  "weaknesses": "<what was missing>",
  "tip": "<one improvement suggestion>"
}}
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)