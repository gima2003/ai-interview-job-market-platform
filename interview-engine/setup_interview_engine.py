import os

HERE = os.path.dirname(os.path.abspath(__file__))

folders = [
    "app",
    "prompts",
    "tests",
]

files = {
    "app/__init__.py": "",

    "app/main.py": '''from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Interview Intelligence Engine")
app.include_router(router)
''',

    "app/routes.py": '''from fastapi import APIRouter
from app.schemas import QuestionRequest, ChatRequest, EvalRequest
from app.question_generator import generate_questions
from app.chatbot import chat_response
from app.evaluator import evaluate_answer

router = APIRouter()

@router.post("/generate-questions")
def get_questions(req: QuestionRequest):
    return generate_questions(req.job_role, req.skills, req.difficulty)

@router.post("/chat")
def chat(req: ChatRequest):
    return chat_response(req.history, req.user_message)

@router.post("/evaluate")
def evaluate(req: EvalRequest):
    return evaluate_answer(req.question, req.user_answer)
''',

    "app/question_generator.py": '''import google.generativeai as genai
import os, json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_questions(job_role: str, skills: list, difficulty: str = "intermediate"):
    prompt = f"""
You are an expert technical interviewer.
Generate interview questions for a {difficulty} {job_role} candidate.
Candidate skills: {", ".join(skills)}

Return ONLY valid JSON in this exact format:
{{
  "technical": ["question1", "question2", "question3"],
  "behavioral": ["question1", "question2"],
  "hr": ["question1", "question2"]
}}
"""
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)
''',

    "app/chatbot.py": '''import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """You are a professional interviewer conducting a mock interview.
Ask follow-up questions based on the candidate answers.
Be constructive, realistic, and concise.
Do not give away answers. Challenge weak responses politely."""

def chat_response(history: list, user_message: str):
    messages = [{"role": "user", "parts": [SYSTEM_PROMPT]}]
    for msg in history:
        messages.append({"role": msg["role"], "parts": [msg["content"]]})
    messages.append({"role": "user", "parts": [user_message]})

    response = model.generate_content(messages)
    return {"reply": response.text}
''',

    "app/evaluator.py": '''import google.generativeai as genai
import os, json
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def evaluate_answer(question: str, user_answer: str):
    prompt = f"""
You are evaluating a mock interview answer.

Question: {question}
Candidate answer: {user_answer}

Return ONLY valid JSON in this exact format:
{{
  "score": <integer 0-10>,
  "strengths": "<what was good>",
  "weaknesses": "<what was missing>",
  "tip": "<one improvement suggestion>"
}}
"""
    response = model.generate_content(prompt)
    text = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(text)
''',

    "app/schemas.py": '''from pydantic import BaseModel

class QuestionRequest(BaseModel):
    job_role: str
    skills: list[str]
    difficulty: str = "intermediate"

class ChatRequest(BaseModel):
    history: list[dict]
    user_message: str

class EvalRequest(BaseModel):
    question: str
    user_answer: str
''',

    "prompts/question_gen.txt": '''You are an expert technical interviewer.
Generate interview questions for a {difficulty} {job_role} candidate.
Candidate skills: {skills}

Return ONLY valid JSON:
{
  "technical": ["question1", "question2", "question3"],
  "behavioral": ["question1", "question2"],
  "hr": ["question1", "question2"]
}
''',

    "prompts/interviewer_system.txt": '''You are a professional interviewer conducting a mock interview.
Ask follow-up questions based on the candidate answers.
Be constructive, realistic, and concise.
Do not give away answers. Challenge weak responses politely.
''',

    "prompts/evaluator.txt": '''You are evaluating a mock interview answer.

Question: {question}
Candidate answer: {user_answer}

Return ONLY valid JSON:
{
  "score": <0-10>,
  "strengths": "<what was good>",
  "weaknesses": "<what was missing>",
  "tip": "<one improvement suggestion>"
}
''',

    "tests/__init__.py": "",

    "tests/test_routes.py": '''from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_questions():
    response = client.post("/generate-questions", json={
        "job_role": "backend developer",
        "skills": ["Python", "FastAPI", "SQL"],
        "difficulty": "intermediate"
    })
    assert response.status_code == 200
    data = response.json()
    assert "technical" in data
    assert "behavioral" in data
''',

    ".env": "GEMINI_API_KEY=your_gemini_api_key_here\n",

    ".gitignore": ".env\n__pycache__/\n*.pyc\nvenv/\n.venv/\n",

    "requirements.txt": "fastapi\nuvicorn\ngoogle-generativeai\nsentence-transformers\npydantic\npython-dotenv\nhttpx\n",

    "README.md": '''# Interview Intelligence Engine — Member 2

## Setup

1. Create and activate virtual environment
```
python -m venv venv
venv\\Scripts\\activate      # Windows
source venv/bin/activate    # Mac/Linux
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Add your Gemini API key to `.env`
```
GEMINI_API_KEY=your_key_here
```

4. Run the server
```
uvicorn app.main:app --reload
```

5. Open API docs at `http://localhost:8000/docs`

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /generate-questions | Generate interview questions |
| POST | /chat | Mock interview chat turn |
| POST | /evaluate | Score a candidate answer |
''',
}

def create():
    for folder in folders:
        path = os.path.join(HERE, folder)
        os.makedirs(path, exist_ok=True)
        print(f"[+] folder   {folder}/")

    for filepath, content in files.items():
        full_path = os.path.join(HERE, filepath)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] file     {filepath}")

    print("\nDone! Run these next:")
    print("  pip install -r requirements.txt")
    print("  uvicorn app.main:app --reload")

if __name__ == "__main__":
    create()
