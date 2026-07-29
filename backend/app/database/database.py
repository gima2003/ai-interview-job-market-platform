import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from pymongo import MongoClient
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Explicitly load .env relative to this file's location
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if MONGODB_URI:
    MONGODB_URI = MONGODB_URI.strip()

DATABASE_NAME = os.getenv("DATABASE_NAME", "ai_career_platform")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is missing or empty. Please check your .env file.")

client = MongoClient(MONGODB_URI)

db = client[DATABASE_NAME]

users_collection = db["users"]
resumes_collection = db["resumes"]
interview_results_collection = db["interview_results"]
job_predictions_collection = db["job_predictions"]
career_roadmaps_collection = db["career_roadmaps"]

print("MongoDB Connected Successfully")