from app.question_generator import generate_questions

result = generate_questions(
    job_role="Backend Developer",
    skills=["Python", "FastAPI", "SQL", "Docker"],
    difficulty="intermediate"
)

print(result)