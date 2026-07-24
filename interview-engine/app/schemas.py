from pydantic import BaseModel

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

class ReportRequest(BaseModel):
    evaluated_answers: list[dict]