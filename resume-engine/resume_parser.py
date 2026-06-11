import fitz
from skill_extractor import extract_skills
from ats_score import calculate_ats_score, find_missing_skills
from report_generator import generate_report
import json
from job_roles import job_roles
from job_matcher import suggest_role


pdf = fitz.open("sample_resume.pdf")

text = ""

for page in pdf:
    text += page.get_text()

pdf.close()

skills = extract_skills(text)
best_role, best_role_score = suggest_role(skills)

target_role = "Data Analyst"
required_skills = job_roles[target_role]

ats_score, matched_skills = calculate_ats_score(skills, required_skills)
missing_skills = find_missing_skills(skills, required_skills)

print("Extracted Skills:")
print(skills)

print("\nMatched Skills:")
print(matched_skills)

print("\nATS Score:")
print(ats_score)

print("\nMissing Skills:")
print(missing_skills)

print("\nBest Matching Role:")
print(best_role)

print("\nBest Role Match Score:")
print(best_role_score)

report = generate_report(
    target_role,
    skills,
    matched_skills,
    missing_skills,
    ats_score,
    best_role,
    best_role_score
)
with open("resume_report.json", "w") as file:
    json.dump(report, file, indent=4)

print("\nReport saved as resume_report.json")

print("\nResume Analysis Report:")
print(report)