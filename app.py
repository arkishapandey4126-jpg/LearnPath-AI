import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Import custom application modules
try:
    from modules.profile import create_profile
    from modules.skill_gap import find_skill_gap
    from modules.roadmap import generate_learning_path
    from modules.resources import get_resources, PROJECTS, ASSESSMENTS
    from modules.persistence import save_state, load_state
except ImportError:
    create_profile = None
    find_skill_gap = None
    generate_learning_path = None
    get_resources = None
    save_state = None
    load_state = None

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LearnPath AI — Editorial Studio",
    page_icon="✦",
    layout="wide"
)

# ============================================================
# STATE PERSISTENCE INITIALIZATION
# ============================================================

if "state_loaded" not in st.session_state:
    if load_state:
        saved_data = load_state()
        if saved_data:
            st.session_state.profile = saved_data.get("profile")
            st.session_state.completed = saved_data.get("completed", set())
            st.session_state.roadmap = saved_data.get("roadmap", [])
            st.session_state.chat_messages = saved_data.get("chat_messages", [])
    st.session_state.state_loaded = True

if "profile" not in st.session_state:
    st.session_state.profile = None

if "roadmap" not in st.session_state:
    st.session_state.roadmap = [
        {"skill": "Python & Data Structures", "hours": 15, "category": "Foundations", "prereqs": []},
        {"skill": "Mathematics & Linear Algebra", "hours": 20, "category": "Foundations", "prereqs": []},
        {"skill": "PyTorch Fundamentals", "hours": 25, "category": "Core Frameworks", "prereqs": ["Python & Data Structures", "Mathematics & Linear Algebra"]},
        {"skill": "Computer Vision & Autoencoders", "hours": 30, "category": "Specialization", "prereqs": ["PyTorch Fundamentals"]},
        {"skill": "FastAPI & Model Deployment", "hours": 15, "category": "Engineering", "prereqs": ["Python & Data Structures"]},
    ]

if "completed" not in st.session_state:
    st.session_state.completed = set(["Python & Data Structures"])

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

# Dynamic Skill Database mapping targets to requirements
SKILL_TARGETS = {
    "AI/ML Engineer": ["Python & Data Structures", "Mathematics & Linear Algebra", "PyTorch Fundamentals", "Computer Vision & Autoencoders", "FastAPI & Model Deployment"],
    "Full-Stack Web Developer": ["HTML/CSS & JavaScript", "TypeScript", "React / Next.js", "Node.js & Express", "MongoDB & REST APIs"],
    "Backend & Cloud Architect": ["Core Java", "Python & Data Structures", "SQL & Relational Databases", "FastAPI & Microservices", "Docker & Kubernetes"],
    "Data Scientist": ["Python & Data Structures", "Mathematics & Linear Algebra", "Pandas & Data Analysis", "Scikit-Learn", "Deep Learning Models"]
}

# ============================================================
# WHITE LILAC (#F8F8F9) & DARK BLUE (#111439) GRADIENT THEME
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --white-lilac: #F8F8F9;
        --dark-blue: #111439;
        --dark-blue-light: #1b1f52;
        --accent-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        --gradient-text: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
    }

    html, body, .stApp {
        background-color: var(--dark-blue) !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.1) 0px, transparent 50%) !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--white-lilac) !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* EDITORIAL FRAMED HERO */
    .hero-frame {
        border: 1px solid rgba(248, 248, 249, 0.25);
        padding: 3rem 2.5rem;
        position: relative;
        margin-bottom: 2.5rem;
        background: rgba(27, 31, 82, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 4px;
    }

    .hero-tag {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #a5b4fc;
        margin-bottom: 1.2rem;
        display: block;
        font-weight: 600;
    }

    .hero-editorial-title {
        font-family: 'Instrument Serif', serif;
        font-size: 4.2rem;
        line-height: 0.95;
        font-weight: 400;
        color: var(--white-lilac);
        margin-bottom: 1.2rem;
        letter-spacing: -0.5px;
    }

    .hero-editorial-title i {
        font-family: 'Instrument Serif', serif;
        font-style: italic;
        background: var(--gradient-text);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-footer-line {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-top: 1.5rem;
        border-top: 1px solid rgba(248, 248, 249, 0.15);
        padding-top: 1rem;
    }

    .hero-arrow {
        font-size: 2rem;
        line-height: 1;
        color: var(--white-lilac);
    }

    /* EDITORIAL GRID CARDS */
    .editorial-grid-card {
        border: 1px solid rgba(248, 248, 249, 0.2);
        padding: 1.8rem;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: rgba(27, 31, 82, 0.5);
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .editorial-grid-card:hover {
        border-color: rgba(192, 132, 252, 0.8);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(17, 20, 57, 0.8);
    }

    .card-num {
        font-family: 'Instrument Serif', serif;
        font-size: 1.8rem;
        color: #94a3b8;
    }

    /* BUTTON STYLING */
    .stButton > button {
        background: transparent !important;
        color: var(--white-lilac) !important;
        border: 1px solid rgba(248, 248, 249, 0.4) !important;
        border-radius: 9999px !important;
        padding: 0.5rem 2rem !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton > button:hover {
        background: var(--accent-gradient) !important;
        color: #ffffff !important;
        border-color: transparent !important;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.4) !important;
    }

    /* Form Controls Styling */
    .stTextInput input, .stSelectbox > div, .stMultiSelect > div, .stTextArea textarea {
        background-color: var(--dark-blue-light) !important;
        border: 1px solid rgba(248, 248, 249, 0.2) !important;
        border-radius: 12px !important;
        color: var(--white-lilac) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b0d26 !important;
        border-right: 1px solid rgba(248, 248, 249, 0.1) !important;
    }

    /* Custom Chat Message Styling */
    div[data-testid="stChatMessage"] {
        background-color: rgba(27, 31, 82, 0.6) !important;
        border: 1px solid rgba(248, 248, 249, 0.15) !important;
        border-radius: 12px !important;
        color: var(--white-lilac) !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# NAVIGATION ROUTER & SIDEBAR DATA ENGINE CONTROLS
# ============================================================

st.sidebar.markdown('### **LEARNPATH AI**')
st.sidebar.markdown('---')

page = st.sidebar.radio(
    "SELECT MODULE",
    [
        "Home",
        "Profile",
        "Skill Gap",
        "Learning Path",
        "Resources",
        "Progress",
        "AI Mentor"
    ]
)

st.sidebar.markdown('---')
st.sidebar.markdown('### **DATA ENGINE**')

if st.sidebar.button("💾 Save Session State"):
    if save_state:
        success = save_state(
            st.session_state.get("profile"),
            st.session_state.get("completed", set()),
            st.session_state.get("roadmap", []),
            st.session_state.get("chat_messages", [])
        )
        if success:
            st.sidebar.success("State saved to disk!")
        else:
            st.sidebar.error("Failed to save state.")
    else:
        st.sidebar.info("Persistence module not imported.")

if st.sidebar.button("🔄 Reset / Clear State"):
    import os
    if os.path.exists("user_state.json"):
        os.remove("user_state.json")
    st.session_state.clear()
    st.rerun()

# ============================================================
# PAGE ROUTING LOGIC
# ============================================================

if page == "Home":
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">✦ SYSTEM ARCHITECTURE</span>
        <div class="hero-editorial-title">
            Architecting Your <br><i>Tech Mastery.</i>
        </div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem; letter-spacing:1px;">LEARNPATH STUDIO / 2026</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('''
        <div class="editorial-grid-card">
            <span class="card-num">01</span>
            <div>
                <h4 style="margin:0; font-weight:600; color: #F8F8F9;">◈ Adaptive Baseline</h4>
                <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.4rem;">Evaluates goals, time commitments, and current technical skills.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        st.markdown('''
        <div class="editorial-grid-card">
            <span class="card-num">02</span>
            <div>
                <h4 style="margin:0; font-weight:600; color: #F8F8F9;">⎔ Gap Diagnostics</h4>
                <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.4rem;">Calculates missing prerequisites across foundational standards.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    with col3:
        st.markdown('''
        <div class="editorial-grid-card">
            <span class="card-num">03</span>
            <div>
                <h4 style="margin:0; font-weight:600; color: #F8F8F9;">✳ Synapse Mentor</h4>
                <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.4rem;">Real-time LLM assistant connected directly to your progress state.</p>
            </div>
        </div>
        ''', unsafe_allow_html=True)

# ------------------------------------------------------------
# MODULE 01: PROFILE
# ------------------------------------------------------------
elif page == "Profile":
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">✦ MODULE / 01</span>
        <div class="hero-editorial-title">Learner <i>Profile.</i></div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem;">CONFIGURE BASELINE</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "Full Name", 
                value=st.session_state.profile.get("name", "") if st.session_state.profile else ""
            )
            goal = st.selectbox(
                "Target Career Track",
                list(SKILL_TARGETS.keys()),
                index=0
            )
            weekly_hours = st.slider("Available Study Hours / Week", 5, 40, 15)

        with col2:
            known_skills = st.multiselect(
                "Current Technical Skills",
                [
                    "Python & Data Structures", "Mathematics & Linear Algebra", "PyTorch Fundamentals",
                    "FastAPI & Model Deployment", "HTML/CSS & JavaScript", "TypeScript",
                    "React / Next.js", "Node.js & Express", "MongoDB & REST APIs",
                    "Core Java", "SQL & Relational Databases", "Pandas & Data Analysis"
                ],
                default=list(st.session_state.completed)
            )
            learning_style = st.select_slider(
                "Preferred Pace & Approach",
                options=["Strict Theory", "Balanced", "Hands-on Project Heavy"]
            )

        # Ensure submit is defined inside the form context
        submit = st.form_submit_button("Save & Calibrate System")

    # Put the form submission handling logic directly here
    if submit:
        st.session_state.profile = {
            "name": name if name else "Learner",
            "goal": goal,
            "weekly_hours": weekly_hours,
            "known_skills": known_skills,
            "learning_style": learning_style
        }
        st.session_state.completed = set(known_skills)
        if generate_learning_path:
            st.session_state.roadmap = generate_learning_path(goal)

        # Auto-save
        if save_state:
            save_state(
                st.session_state.profile, 
                st.session_state.completed, 
                st.session_state.roadmap, 
                st.session_state.get("chat_messages", [])
            )
        st.success("Profile saved and baseline calibrated!")
            
# ------------------------------------------------------------
# MODULE 02: SKILL GAP
# ------------------------------------------------------------
elif page == "Skill Gap":
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">⎔ MODULE / 02</span>
        <div class="hero-editorial-title">Skill Gap <i>Diagnostics.</i></div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem;">MISSING PREREQUISITES</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if not st.session_state.profile:
        st.info("ℹ️ Complete your **Profile** module first to generate a personalized skill gap diagnosis.")
    else:
        profile = st.session_state.profile
        target_role = profile["goal"]
        required_skills = SKILL_TARGETS.get(target_role, [])
        acquired = set(profile["known_skills"])
        missing = [s for s in required_skills if s not in acquired]

        st.subheader(f"Target Role Diagnostic: **{target_role}**")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Required Skills", len(required_skills))
        c2.metric("Acquired Mastery", len(acquired))
        c3.metric("Identified Gaps", len(missing))

        st.markdown("### Baseline Readiness Breakdown")
        
        for skill in required_skills:
            if skill in acquired:
                st.markdown(f"✅ **{skill}** — *Competency Confirmed*")
            else:
                st.markdown(f"⚠️ <span style='color:#ec4899; font-weight:600;'>{skill}</span> — *Skill Gap (Action Required)*", unsafe_allow_html=True)

# ------------------------------------------------------------
# MODULE 03: LEARNING PATH (Roadmap Graph & Table)
# ------------------------------------------------------------
elif page == "Learning Path":
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">⚡ MODULE / 03</span>
        <div class="hero-editorial-title">Dynamic <i>Roadmap.</i></div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem;">GRAPH ROUTING & DEPENDENCY TREE</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.subheader("Prerequisite Network Graph")

    G = nx.DiGraph()
    for item in st.session_state.roadmap:
        G.add_node(item["skill"])
        for prereq in item["prereqs"]:
            G.add_edge(prereq, item["skill"])

    fig, ax = plt.subplots(figsize=(10, 4.5), facecolor='#111439')
    ax.set_facecolor('#111439')
    
    pos = nx.spring_layout(G, seed=42)
    # Active accent (#c084fc) for completed, slate (#1b1f52) for pending
    node_colors = ['#c084fc' if node in st.session_state.completed else '#1b1f52' for node in G.nodes()]
    edge_colors = '#6366f1'
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2200, edgecolors='#F8F8F9', linewidths=1.5, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=2, arrowsize=15, ax=ax)
    nx.draw_networkx_labels(G, pos, font_color='#F8F8F9', font_size=8, font_family='sans-serif', ax=ax)
    
    plt.axis('off')
    st.pyplot(fig)

    st.markdown("### Planned Curriculum & Milestones")
    roadmap_df = pd.DataFrame(st.session_state.roadmap)
    roadmap_df["Status"] = roadmap_df["skill"].apply(lambda x: "Completed" if x in st.session_state.completed else "In Progress")
    st.dataframe(roadmap_df, use_container_width=True)

# ------------------------------------------------------------
# MODULE 04: RESOURCES
# ------------------------------------------------------------
elif page == "Resources":
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">✸ MODULE / 04</span>
        <div class="hero-editorial-title">Curated <i>Vault.</i></div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem;">RESOURCES & PRACTICAL PROJECTS</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📚 Core Learning Material", "🛠️ Hands-on Projects"])

    with tab1:
        st.markdown("""
        * **PyTorch Documentation & Deep Learning Tutorials** — Official docs and practice labs.
        * **FastAPI Microservice Architecture** — Building production-ready model endpoints.
        * **Variational Autoencoders & Computer Vision** — Applied generative models step-by-step.
        """)

    with tab2:
        st.markdown("""
        * **Real-Time Fraud Detection REST API** (PyTorch + FastAPI + Pydantic)
        * **Health Nexus Management System** (MERN Stack Architecture)
        * **AI-Powered Trip Planner Studio** (Next.js + Mapbox API)
        """)

# ------------------------------------------------------------
# MODULE 05: PROGRESS
# ------------------------------------------------------------
elif page == "Progress":
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">MODULE / 05</span>
        <div class="hero-editorial-title">Analytics & <i>Metrics.</i></div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem;">PROGRESS TRACKER</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    total_skills = len(st.session_state.roadmap)
    completed_cnt = len(st.session_state.completed)
    pct = (completed_cnt / total_skills) if total_skills > 0 else 0.0

    st.metric("Total Progress", f"{int(pct * 100)}%")
    st.progress(pct)

    st.markdown("### Skill Checklist")

    # Callback function to handle checkbox state toggling directly
    def on_skill_toggle(skill_name):
        cb_key = f"chk_{skill_name}"
        if st.session_state.get(cb_key):
            st.session_state.completed.add(skill_name)
        else:
            st.session_state.completed.discard(skill_name)
            
        # Save state automatically on change
        if save_state:
            save_state(
                st.session_state.profile,
                st.session_state.completed,
                st.session_state.roadmap,
                st.session_state.get("chat_messages", [])
            )

    # Render checklist items
    for item in st.session_state.roadmap:
        skill = item["skill"]
        is_done = skill in st.session_state.completed
        cb_key = f"chk_{skill}"

        st.checkbox(
            f"**{skill}** ({item['hours']} hrs)",
            value=is_done,
            key=cb_key,
            on_change=on_skill_toggle,
            args=(skill,)
        )

# ------------------------------------------------------------
# MODULE 06: AI MENTOR
# ------------------------------------------------------------
elif page == "AI Mentor":
    st.markdown('''
    <div class="hero-frame">
        <span class="hero-tag">✦ MODULE / 06</span>
        <div class="hero-editorial-title">AI <i>Mentor.</i></div>
        <div class="hero-footer-line">
            <span style="color:#94a3b8; font-size:0.9rem;">CONTEXT-AWARE ADVISOR</span>
            <span class="hero-arrow">↓</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display existing messages
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input box
    if prompt := st.chat_input("Ask your mentor anything about your learning path..."):
        # Display user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response using OpenAI integration
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response_text = generate_ai_response(
                    st.session_state.chat_messages,
                    st.session_state.profile,
                    st.session_state.roadmap,
                    st.session_state.completed
                )
                st.write(response_text)
                st.session_state.chat_messages.append({"role": "assistant", "content": response_text})

        # Save state after message exchange
        if save_state:
            save_state(
                st.session_state.profile,
                st.session_state.completed,
                st.session_state.roadmap,
                st.session_state.chat_messages
            )