import os
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types


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
        # Normalize role: Gemini API requires 'user' or 'model' (not 'assistant' or 'bot')
        role = "model" if msg.get("role") in ["assistant", "bot", "model"] else "user"
        content_text = msg.get("content", "")
        messages.append(
            types.Content(
                role=role,
                parts=[types.Part(text=content_text)]
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

        reply_text = response.text if response and response.text else "Sorry, I could not generate a response. Please try again."
        return {"reply": reply_text}

    except Exception as e:
        print(f"Chatbot error: {e}")
        return {"reply": "Sorry, I encountered an error processing your request. Please try again."}
