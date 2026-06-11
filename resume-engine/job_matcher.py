from job_roles import job_roles

def suggest_role(user_skills):

    best_role = ""
    best_score = 0

    for role, required_skills in job_roles.items():

        matched_count = 0

        for skill in required_skills:
            if skill in user_skills:
                matched_count += 1

        score = (matched_count / len(required_skills)) * 100

        if score > best_score:
            best_score = score
            best_role = role

    return best_role, round(best_score)