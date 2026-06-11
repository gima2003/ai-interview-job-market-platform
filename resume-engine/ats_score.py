def calculate_ats_score(user_skills, required_skills):
    matched_skills = []

    for skill in required_skills:
        if skill in user_skills:
            matched_skills.append(skill)

    score = (len(matched_skills) / len(required_skills)) * 100

    return round(score), matched_skills


def find_missing_skills(user_skills, required_skills):
    missing_skills = []

    for skill in required_skills:
        if skill not in user_skills:
            missing_skills.append(skill)

    return missing_skills