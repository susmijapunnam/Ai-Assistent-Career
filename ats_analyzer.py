def calculate_ats_score(resume_text, skills):

    score = 0

    if len(resume_text) > 500:
        score += 20

    if len(skills) >= 5:
        score += 20

    if "project" in resume_text.lower():
        score += 20

    if "education" in resume_text.lower():
        score += 20

    if "experience" in resume_text.lower():
        score += 20

    return min(score, 100)
