import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a professional interviewer conducting a mock interview.
Ask follow-up questions based on the candidate answers.
Be constructive, realistic, and concise.
Do not give away answers. Challenge weak responses politely."""

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

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=messages
    )
    return {"reply": response.text}