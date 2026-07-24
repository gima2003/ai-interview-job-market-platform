import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a professional technical interviewer conducting a mock interview.
Your job is to ask one question at a time and evaluate the candidate's responses.

Rules:
- Ask focused follow-up questions based on what the candidate says.
- If an answer is weak or vague, probe deeper — don't accept surface-level answers.
- Never give away the answer or hint at what a good answer looks like.
- Be professional but direct.
- Keep your responses concise — one follow-up or one new question per turn.
- Only ask questions relevant to the candidate's stated skills and role."""

def chat_response(history: list, user_message: str):
    messages = []

    for msg in history:
        messages.append(
            types.Content(
                role=msg["role"],
                parts=[types.Part(text=msg["content"])]
            )
        )

    messages.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
    )

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT
            ),
            contents=messages
        )

        return {"reply": response.text}

    except Exception as e:
        print(f"Chatbot error: {e}")
        return {"reply": "Sorry, I encountered an error. Please try again."}