# ============================================================
# ROLE SKILLS
# ============================================================

ROLE_SKILLS = {

    "Machine Learning Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Statistics",
        "Machine Learning",
        "Scikit-learn",
        "Deep Learning",
        "TensorFlow"
    ],

    "Data Scientist": [
        "Python",
        "NumPy",
        "Pandas",
        "Statistics",
        "SQL",
        "Machine Learning",
        "Scikit-learn"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "Statistics",
        "Data Visualization"
    ],

    "AI Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "NLP",
        "Generative AI"
    ],

    "NLP Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Transformers"
    ],

    "Computer Vision Engineer": [
        "Python",
        "NumPy",
        "Pandas",
        "Machine Learning",
        "Deep Learning",
        "Computer Vision",
        "TensorFlow"
    ]
}


# ============================================================
# ROLE DETECTION
# ============================================================

def detect_role(goal):

    text = goal.lower()

    if "machine learning engineer" in text:
        return "Machine Learning Engineer"

    elif "ml engineer" in text:
        return "Machine Learning Engineer"

    elif "machine learning developer" in text:
        return "Machine Learning Engineer"

    elif "data scientist" in text:
        return "Data Scientist"

    elif "data science" in text:
        return "Data Scientist"

    elif "data analyst" in text:
        return "Data Analyst"

    elif "data analysis" in text:
        return "Data Analyst"

    elif "ai engineer" in text:
        return "AI Engineer"

    elif "artificial intelligence engineer" in text:
        return "AI Engineer"

    elif "ai developer" in text:
        return "AI Engineer"

    elif "nlp engineer" in text:
        return "NLP Engineer"

    elif "natural language processing" in text:
        return "NLP Engineer"

    elif "computer vision engineer" in text:
        return "Computer Vision Engineer"

    elif "computer vision" in text:
        return "Computer Vision Engineer"

    elif "machine learning" in text:
        return "Machine Learning Engineer"

    elif "artificial intelligence" in text:
        return "AI Engineer"

    return None


# ============================================================
# SKILL GAP FUNCTION
# ============================================================

def find_skill_gap(goal, current_skills):

    role = detect_role(goal)

    # ALWAYS RETURN 4 VALUES
    if role is None:
        return [], [], [], None

    required_skills = ROLE_SKILLS[role]

    current_lower = {
        skill.strip().lower()
        for skill in current_skills
    }

    completed_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill.lower() in current_lower:
            completed_skills.append(skill)

        else:
            missing_skills.append(skill)

    # ALWAYS RETURN 4 VALUES
    return (
        required_skills,
        completed_skills,
        missing_skills,
        role
    )