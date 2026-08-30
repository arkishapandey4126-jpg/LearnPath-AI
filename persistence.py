# modules/persistence.py
import json
import os

STATE_FILE = "user_state.json"

def save_state(profile, completed, roadmap, chat_messages):
    try:
        data = {
            "profile": profile,
            "completed": list(completed) if isinstance(completed, set) else completed,
            "roadmap": roadmap,
            "chat_messages": chat_messages
        }
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving state: {e}")
        return False

def load_state():
    if not os.path.exists(STATE_FILE):
        return None
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["completed"] = set(data.get("completed", []))
            return data
    except Exception as e:
        print(f"Error loading state: {e}")
        return None