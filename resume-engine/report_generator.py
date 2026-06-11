def generate_report(target_role, skills, matched_skills, missing_skills, ats_score, best_role, best_role_score):
    report = {
        "target_role": target_role,
        "extracted_skills": skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "ats_score": ats_score,
        "best_matching_role": best_role,
        "best_role_score": best_role_score
    }

    return report