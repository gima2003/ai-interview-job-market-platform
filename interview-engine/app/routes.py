from fastapi import APIRouter, HTTPException
from app.schemas import QuestionRequest, ChatRequest, EvalRequest, ReportRequest
from app.question_generator import generate_questions
from app.chatbot import chat_response
from app.evaluator import evaluate_answer, generate_feedback_report

router = APIRouter()


@router.post("/generate-questions")
def get_questions(req: QuestionRequest):
    result = generate_questions(req.job_role, req.skills, req.difficulty)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/chat")
def chat(req: ChatRequest):
    result = chat_response(req.history, req.user_message)
    if "error" in result.get("reply", ""):
        raise HTTPException(status_code=500, detail=result["reply"])
    return result


@router.post("/evaluate")
def evaluate(req: EvalRequest):
    result = evaluate_answer(req.question, req.user_answer)
    if result.get("strengths") == "Error occurred":
        raise HTTPException(status_code=500, detail="Evaluation failed")
    return result


@router.post("/report")
def report(req: ReportRequest):
    result = generate_feedback_report(req.evaluated_answers)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result