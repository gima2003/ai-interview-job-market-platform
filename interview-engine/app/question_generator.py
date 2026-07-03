import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_questions(job_role: str, skills: list, difficulty: str = "intermediate"):
    prompt = f"""
You are a senior technical interviewer with 10 years of experience hiring for {job_role} roles.

Generate exactly 3 technical questions, 2 behavioral questions, and 2 HR questions
for a {difficulty} level candidate.

Candidate's skills: {", ".join(skills)}

Rules:
- Do NOT include answers.
- Do NOT add any explanation, greeting, or extra text.
- Base technical questions on the candidate's actual skills listed above.

Return ONLY valid JSON in this exact format, nothing else:
{{
  "technical": ["question1", "question2", "question3"],
  "behavioral": ["question1", "question2"],
  "hr": ["question1", "question2"]
}}
"""
    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        text = response.text.strip()
        text = text.replace("```json", "")
        text = text.replace("```", "")

        return json.loads(text)

    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {"error": str(e)}