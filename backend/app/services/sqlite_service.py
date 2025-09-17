import sqlite3
import json
from datetime import date, datetime
from typing import Optional, List, Dict
from backend.app.models.user import UserProfile

DB_PATH = "backend/app/services/user_profiles.db"

def dict_to_userprofile(data: Dict) -> UserProfile:
    profile = UserProfile()
    for key, value in data.items():
        if hasattr(profile, key):
            # Handle special types
            if key == "date_of_birth" and value:
                try:
                    profile.date_of_birth = datetime.strptime(value, "%Y-%m-%d").date()
                except Exception:
                    profile.date_of_birth = None
            elif key in [
                "sub_goals", "available_equipment", "special_conditions",
                "allergies", "diseases", "dietary_preferences"
            ] and isinstance(value, str):
                setattr(profile, key, json.loads(value))
            else:
                setattr(profile, key, value)
    return profile

def userprofile_to_dict(profile: UserProfile) -> Dict:
    d = profile.to_dict()
    # Serialize lists as JSON strings
    for key in [
        "sub_goals", "available_equipment", "special_conditions",
        "allergies", "diseases", "dietary_preferences"
    ]:
        d[key] = json.dumps(d[key])
    # Serialize date
    if d["date_of_birth"]:
        d["date_of_birth"] = d["date_of_birth"]
    return d

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        date_of_birth TEXT,
        gender TEXT,
        height REAL,
        weight REAL,
        fitness_goals TEXT,
        sub_goals TEXT,
        activity_level TEXT,
        experience_level TEXT,
        training_days INTEGER,
        time_per_session INTEGER,
        workout_location TEXT,
        available_equipment TEXT,
        special_conditions TEXT,
        allergies TEXT,
        diseases TEXT,
        dietary_preferences TEXT,
        cooking_time INTEGER,
        user_background TEXT
    )
    """)
    conn.commit()
    conn.close()

def create_user(profile: UserProfile) -> int:
    init_db()
    d = userprofile_to_dict(profile)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    columns = ', '.join(d.keys())
    placeholders = ', '.join(['?'] * len(d))
    values = list(d.values())
    c.execute(f"INSERT INTO user_profiles ({columns}) VALUES ({placeholders})", values)
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

def get_user(user_id: int) -> Optional[UserProfile]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        keys = [desc[0] for desc in c.description]
        data = dict(zip(keys, row))
        return dict_to_userprofile(data)
    return None

def update_user(user_id: int, profile: UserProfile) -> bool:
    init_db()
    d = userprofile_to_dict(profile)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    assignments = ', '.join([f"{k}=?" for k in d.keys()])
    values = list(d.values()) + [user_id]
    c.execute(f"UPDATE user_profiles SET {assignments} WHERE id = ?", values)
    conn.commit()
    updated = c.rowcount > 0
    conn.close()
    return updated

def delete_user(user_id: int) -> bool:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM user_profiles WHERE id = ?", (user_id,))
    conn.commit()
    deleted = c.rowcount > 0
    conn.close()
    return deleted

def list_users() -> List[UserProfile]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM user_profiles")
    rows = c.fetchall()
    conn.close()
    profiles = []
    for row in rows:
        keys = [desc[0] for desc in c.description]
        data = dict(zip(keys, row))
        profiles.append(dict_to_userprofile(data))
    return profiles