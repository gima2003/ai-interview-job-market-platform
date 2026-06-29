import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_questions(job_role: str, skills: list, difficulty: str = "intermediate"):
    prompt = f"""
You are an expert technical interviewer.
Generate interview questions for a {difficulty} {job_role} candidate.
Candidate skills: {", ".join(skills)}

Return ONLY valid JSON in this exact format, no extra text:
{{
  "technical": ["question1", "question2", "question3"],
  "behavioral": ["question1", "question2"],
  "hr": ["question1", "question2"]
}}
"""
    response = client.models.generate_content(
       model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)