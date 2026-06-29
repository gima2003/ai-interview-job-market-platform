from fastapi import APIRouter
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
