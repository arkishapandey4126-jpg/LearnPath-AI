import streamlit as st
import pandas as pd
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
COURSES_PATH = os.path.join(DATA_DIR, "courses.csv")
RESOURCES_PATH = os.path.join(DATA_DIR, "resources.csv")

@st.cache_data
def load_csv_data():
    """Loads courses and resources CSV datasets with caching."""
    courses_df = pd.read_csv(COURSES_PATH) if os.path.exists(COURSES_PATH) else pd.DataFrame()
    resources_df = pd.read_csv(RESOURCES_PATH) if os.path.exists(RESOURCES_PATH) else pd.DataFrame()
    return courses_df, resources_df

def render_resources_tab(profile, roadmap, completed_skills):
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">✦ MODULE / 04</span>
        <div class="hero-editorial-title">Curated <i>Resources.</i></div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem;">RECOMMENDED LEARNING MATERIAL</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    courses_df, resources_df = load_csv_data()

    if courses_df.empty and resources_df.empty:
        st.warning("No resource datasets found in `data/` folder.")
        return

    # Filter resources for pending skills
    pending_skills = [item["skill"] for item in roadmap if item["skill"] not in completed_skills]
    
    st.markdown("### ✸ Recommended Courses & Material")
    
    selected_skill = st.selectbox("Filter resources by Skill:", ["All Pending Skills"] + pending_skills)

    # Display resources
    df_to_show = resources_df if not resources_df.empty else courses_df

    if selected_skill != "All Pending Skills" and "skill" in df_to_show.columns:
        filtered_df = df_to_show[df_to_show["skill"].str.lower() == selected_skill.lower()]
    else:
        filtered_df = df_to_show

    st.dataframe(filtered_df, use_container_width=True)