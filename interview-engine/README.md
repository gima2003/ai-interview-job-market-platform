# Interview Intelligence Engine — Member 2

## Setup

1. Create and activate virtual environment
```
python -m venv venv
venv\Scripts\activate      # Windows
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
