def create_profile(
    name,
    goal,
    experience,
    skills,
    interests,
    completed_courses,
    weekly_hours,
    timeline,
    learning_preference,
    free_only
):

    profile = {
        "name": name,
        "goal": goal,
        "experience": experience,
        "skills": skills,
        "interests": interests,
        "completed_courses": completed_courses,
        "weekly_hours": weekly_hours,
        "timeline": timeline,
        "learning_preference": learning_preference,
        "free_only": free_only
    }

    return profile