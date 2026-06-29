from fastapi.testclient import TestClient
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
