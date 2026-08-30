import streamlit as st
from openai import OpenAI

def get_ai_client():
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key missing. Please add `OPENAI_API_KEY` to `.streamlit/secrets.toml`.")
        return None
    return OpenAI(api_key=api_key)

def generate_ai_response(messages, profile, roadmap, completed_skills):
    """
    Generates tailored advice using OpenAI GPT models based on the learner's context.
    """
    client = get_ai_client()
    if not client:
        return "API key not configured."

    # Context assembly from learner profile & roadmap
    name = profile.get("name", "Learner")
    goal = profile.get("goal", "AI/ML Engineer")
    style = profile.get("learning_style", "Balanced")
    
    all_skills = [item["skill"] for item in roadmap]
    pending_skills = [s for s in all_skills if s not in completed_skills]
    
    system_prompt = (
        f"You are an expert AI Learning Assistant & Technical Mentor.\n"
        f"Learner Name: {name}\n"
        f"Target Goal: {goal}\n"
        f"Learning Style: {style}\n"
        f"Completed Skills: {list(completed_skills)}\n"
        f"Remaining Roadmap Skills: {pending_skills}\n\n"
        f"Provide concise, actionable advice. Encourage hands-on project building."
    )

    # Prepare chat history for OpenAI API
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in messages:
        api_messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fast and cost-effective; switch to "gpt-4o" if preferred
            messages=api_messages,
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with AI Assistant: {e}"