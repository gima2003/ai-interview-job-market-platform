def extract_skills(resume_text):
    skill_keywords = [
        "python", "java", "javascript", "c", "c++",
        "react", "next.js", "tailwind css",
        "node.js", "express.js", "spring boot",
        "mysql", "mongodb",
        "power bi", "excel",
        "ssis", "ssas",
        "data warehousing", "etl",
        "data visualization",
        "statistical analysis",
        "machine learning", "nlp",
        "git", "vs code", "figma"
    ]

    found_skills = []

    resume_text = resume_text.lower()

    for skill in skill_keywords:
        if skill in resume_text:
            found_skills.append(skill)

    return found_skills