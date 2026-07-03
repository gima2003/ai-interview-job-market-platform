import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def evaluate_answer(question: str, user_answer: str):
    prompt = f"""
You are an expert technical interviewer evaluating a candidate's interview answer.

Question asked: {question}
Candidate's answer: {user_answer}

Evaluate the answer strictly and fairly using this scoring rubric:
- 9-10: Complete and accurate, includes edge cases and real-world context
- 7-8:  Correct core answer with only minor gaps
- 5-6:  Partially correct, missing key concepts
- 3-4:  Shows some understanding but has significant gaps
- 1-2:  Mostly incorrect or irrelevant to the question
- 0:    No attempt or completely wrong

Return ONLY valid JSON, no extra text, no markdown:
{{
  "score": <integer from 0 to 10>,
  "strengths": "<one sentence about what the candidate got right>",
  "weaknesses": "<one sentence about what was missing or wrong>",
  "tip": "<one specific actionable improvement suggestion>"
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

    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw response was: {response.text}")
        return {
            "score": 0,
            "strengths": "Could not evaluate",
            "weaknesses": "Could not evaluate",
            "tip": "Please try again"
        }

    except Exception as e:
        print(f"Evaluator error: {e}")
        return {
            "score": 0,
            "strengths": "Error occurred",
            "weaknesses": "Error occurred",
            "tip": "Please try again"
        }


def generate_feedback_report(evaluated_answers: list):
    if not evaluated_answers:
        return {"error": "No answers to evaluate"}

    total_score = sum(a["score"] for a in evaluated_answers)
    average_score = round(total_score / len(evaluated_answers), 1)

    prompt = f"""
You are an expert career coach summarizing a mock interview performance.

The candidate answered {len(evaluated_answers)} questions with an average score of {average_score}/10.

Individual scores: {[a["score"] for a in evaluated_answers]}
Key weaknesses identified: {[a["weaknesses"] for a in evaluated_answers]}

Write a brief overall summary (2-3 sentences) of the candidate's performance.
Be honest but encouraging. Focus on the most important area to improve.

Return ONLY valid JSON, no extra text:
{{
  "overall_score": {average_score},
  "total_questions": {len(evaluated_answers)},
  "summary": "<2-3 sentence overall performance summary>",
  "top_tip": "<the single most important thing they should work on>"
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

        report = json.loads(text)
        report["answers"] = evaluated_answers
        return report

    except Exception as e:
        print(f"Report generation error: {e}")
        return {
            "overall_score": average_score,
            "total_questions": len(evaluated_answers),
            "summary": "Could not generate summary",
            "top_tip": "Please review individual feedback",
            "answers": evaluated_answers
        }