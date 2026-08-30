import networkx as nx

# Comprehensive Master Skill Catalog with explicit prerequisite relations
SKILL_CATALOG = {
    "AI/ML Engineer": [
        {"skill": "Python & Data Structures", "hours": 15, "category": "Foundations", "prereqs": []},
        {"skill": "Mathematics & Linear Algebra", "hours": 20, "category": "Foundations", "prereqs": []},
        {"skill": "PyTorch Fundamentals", "hours": 25, "category": "Core Frameworks", "prereqs": ["Python & Data Structures", "Mathematics & Linear Algebra"]},
        {"skill": "Computer Vision & Autoencoders", "hours": 30, "category": "Specialization", "prereqs": ["PyTorch Fundamentals"]},
        {"skill": "FastAPI & Model Deployment", "hours": 15, "category": "Engineering", "prereqs": ["Python & Data Structures"]},
    ],
    "Full-Stack Web Developer": [
        {"skill": "HTML/CSS & JavaScript", "hours": 15, "category": "Foundations", "prereqs": []},
        {"skill": "TypeScript", "hours": 15, "category": "Foundations", "prereqs": ["HTML/CSS & JavaScript"]},
        {"skill": "React / Next.js", "hours": 25, "category": "Frontend", "prereqs": ["TypeScript"]},
        {"skill": "Node.js & Express", "hours": 20, "category": "Backend", "prereqs": ["HTML/CSS & JavaScript"]},
        {"skill": "MongoDB & REST APIs", "hours": 15, "category": "Database", "prereqs": ["Node.js & Express"]},
    ],
    "Backend & Cloud Architect": [
        {"skill": "Core Java", "hours": 20, "category": "Foundations", "prereqs": []},
        {"skill": "SQL & Relational Databases", "hours": 15, "category": "Databases", "prereqs": []},
        {"skill": "Python & Data Structures", "hours": 15, "category": "Foundations", "prereqs": []},
        {"skill": "FastAPI & Microservices", "hours": 20, "category": "Backend", "prereqs": ["Python & Data Structures", "SQL & Relational Databases"]},
        {"skill": "Docker & Kubernetes", "hours": 25, "category": "DevOps & Cloud", "prereqs": ["FastAPI & Microservices"]},
    ],
    "Data Scientist": [
        {"skill": "Python & Data Structures", "hours": 15, "category": "Foundations", "prereqs": []},
        {"skill": "Mathematics & Linear Algebra", "hours": 20, "category": "Foundations", "prereqs": []},
        {"skill": "Pandas & Data Analysis", "hours": 15, "category": "Data Wrangling", "prereqs": ["Python & Data Structures"]},
        {"skill": "Scikit-Learn", "hours": 20, "category": "Machine Learning", "prereqs": ["Pandas & Data Analysis", "Mathematics & Linear Algebra"]},
        {"skill": "Deep Learning Models", "hours": 30, "category": "Advanced ML", "prereqs": ["Scikit-Learn"]},
    ]
}


def build_dependency_graph(skills_list):
    """
    Constructs a Directed Acyclic Graph (DAG) using NetworkX from a list of skill dicts.
    """
    G = nx.DiGraph()
    for item in skills_list:
        G.add_node(item["skill"], data=item)
        for prereq in item.get("prereqs", []):
            G.add_edge(prereq, item["skill"])
    return G


def generate_learning_path(target_role):
    """
    Generates a topologically sorted learning path based on dependency ordering.
    
    Parameters:
        target_role (str): The career path chosen by the user (e.g., 'AI/ML Engineer')
        
    Returns:
        list: A topologically ordered list of skill dictionaries.
    """
    raw_skills = SKILL_CATALOG.get(target_role, SKILL_CATALOG["AI/ML Engineer"])
    
    # Construct NetworkX Graph
    G = build_dependency_graph(raw_skills)
    
    try:
        # Perform Topological Sort to derive valid execution order
        ordered_skill_names = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible:
        # Fallback if circular dependency is detected
        ordered_skill_names = [item["skill"] for item in raw_skills]

    # Map ordered names back to full skill dictionary objects
    skill_map = {item["skill"]: item for item in raw_skills}
    ordered_path = [skill_map[name] for name in ordered_skill_names if name in skill_map]

    return ordered_path