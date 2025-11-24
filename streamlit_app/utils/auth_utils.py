# streamlit_app/utils/auth_utils.py
import streamlit as st
from pathlib import Path
import json
import bcrypt  # optional: install bcrypt for proper password hashing
from typing import Optional
from streamlit_app.utils.data_access import load_json, write_json

USERS_PATH = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db" / "users.json"

def ensure_session():
    if "auth" not in st.session_state:
        st.session_state.auth = {"logged_in": False, "user_id": None}

def get_users():
    data = load_json(USERS_PATH)
    return data.get("users", [])

def find_user_by_email(email: str) -> Optional[dict]:
    for u in get_users():
        if u["email"].lower() == email.lower():
            return u
    return None

def verify_password(plain: str, hashed: str) -> bool:
    try:
        # bcrypt hashed password
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        # fallback - simulation only (NOT SECURE)
        return plain == hashed

def login(email: str, password: str) -> bool:
    user = find_user_by_email(email)
    if not user:
        return False
    if verify_password(password, user["password_hash"]):
        st.session_state.auth = {"logged_in": True, "user_id": user["id"]}
        return True
    return False

def logout():
    st.session_state.auth = {"logged_in": False, "user_id": None}

def is_logged_in() -> bool:
    ensure_session()
    return st.session_state.auth.get("logged_in", False)

def get_current_user() -> Optional[dict]:
    ensure_session()
    uid = st.session_state.auth.get("user_id")
    if not uid:
        return None
    for u in get_users():
        if u["id"] == uid:
            return u
    return None

# RBAC: define which pages require which roles (simplified)
PAGE_ROLE_MAP = {
    "Dashboard": ["Admin", "Company", "Company_Aggregator", "Auditor"],
    "Assessment (Level 1)": ["Company"],
    "Assessment (Level 2)": ["Company", "Auditor"],
    "Upload Document": ["Company"],
    "OCR Processor": ["Auditor", "Admin"],
    "Aggregator Overview": ["Company_Aggregator"],
    "Question Editor (Admin)": ["Admin"],
    "User Manager (Admin)": ["Admin"],
    "Industry Clustering": ["Admin"],
    "API Diagnostics": ["Admin"]
}

def require_roles_for_page(page_name: str, user: Optional[dict]) -> bool:
    """
    Return True if page is public (Login) or user has one of required roles.
    If page not in map, default to allow.
    """
    if page_name == "Login":
        return True
    required = PAGE_ROLE_MAP.get(page_name)
    if not required:
        return True
    if not user:
        return False
    user_roles = user.get("roles", [])
    return any(r in user_roles for r in required)