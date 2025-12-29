# streamlit_app/utils/auth_utils.py

import os
import streamlit as st
from pathlib import Path
from typing import Optional

from streamlit_app.utils.data_access import load_json, write_json

# ============================================================
# FORCE DEV MODE (NO BCRYPT, NO AUTO DETECTION)
# ============================================================
DEV_MODE = True   # ← THIS OVERRIDES EVERYTHING

# ============================================================
# PATHS
# ============================================================
DB_ROOT = Path(os.getcwd()) / "backend" / "db" / "json_db"
USERS_PATH = DB_ROOT / "users.json"

# ============================================================
# SESSION
# ============================================================
def ensure_session():
    if "auth" not in st.session_state:
        st.session_state.auth = {
            "logged_in": False,
            "user_id": None,
        }

# ============================================================
# USERS
# ============================================================
def get_users():
    data = load_json(USERS_PATH)
    return data.get("users", [])

def find_user_by_email(email: str) -> Optional[dict]:
    for u in get_users():
        if u["email"].lower() == email.lower():
            return u
    return None

# ============================================================
# PASSWORD CHECK (FORCED DEV)
# ============================================================
def verify_password(plain: str, stored: str) -> bool:
    plain = plain.strip()
    stored = stored.strip()
    return plain == stored

# ============================================================
# LOGIN
# ============================================================
def login(email: str, password: str) -> bool:
    ensure_session()

    users = get_users()
    st.session_state["_DEBUG_USERS"] = users  # ← visible proof

    user = find_user_by_email(email)

    if not user:
        st.session_state["_DEBUG_REASON"] = "User not found"
        return False

    ok = verify_password(password, user.get("password_hash", ""))

    st.session_state["_DEBUG_PASSWORD_OK"] = ok
    st.session_state["_DEBUG_EXPECTED"] = user.get("password_hash")
    st.session_state["_DEBUG_INPUT"] = password

    if ok:
        st.session_state.auth = {
            "logged_in": True,
            "user_id": user["id"],
        }
        return True

    return False

# ============================================================
# STATE HELPERS
# ============================================================
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

# ============================================================
# RBAC
# ============================================================
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
    "API Diagnostics": ["Admin"],
}

def require_roles_for_page(page_name: str, user: Optional[dict]) -> bool:
    if page_name == "Login":
        return True
    required = PAGE_ROLE_MAP.get(page_name)
    if not required:
        return True
    if not user:
        return False
    return any(r in user.get("roles", []) for r in required)


# # streamlit_app/utils/auth_utils.py

# import os
# import streamlit as st
# from pathlib import Path
# from typing import Optional

# from streamlit_app.utils.data_access import load_json, write_json

# # ============================================================
# # AUTH CONFIG (DEV MODE)
# # ============================================================
# # IMPORTANT:
# # We explicitly disable bcrypt because users.json contains
# # placeholder hashes like "HASH_ADMIN".
# # This avoids bcrypt.checkpw() failures.

# _HAS_BCRYPT = False   # ← THIS IS THE KEY FIX

# # ============================================================
# # PATHS
# # ============================================================
# DB_ROOT = Path(os.getcwd()) / "backend" / "db" / "json_db"
# USERS_PATH = DB_ROOT / "users.json"

# # ============================================================
# # SESSION
# # ============================================================
# def ensure_session():
#     if "auth" not in st.session_state:
#         st.session_state.auth = {
#             "logged_in": False,
#             "user_id": None,
#         }

# # ============================================================
# # USERS
# # ============================================================
# def get_users():
#     data = load_json(USERS_PATH)
#     return data.get("users", [])

# def find_user_by_email(email: str) -> Optional[dict]:
#     for u in get_users():
#         if u["email"].lower() == email.lower():
#             return u
#     return None

# # ============================================================
# # PASSWORD HANDLING (DEV)
# # ============================================================
# def verify_password(plain: str, stored: str) -> bool:
#     """
#     DEV MODE:
#     - stored value is treated as plain text
#     - e.g. HASH_ADMIN == HASH_ADMIN
#     """
#     return plain == stored

# # ============================================================
# # LOGIN / LOGOUT
# # ============================================================
# def login(email: str, password: str) -> bool:
#     ensure_session()
#     user = find_user_by_email(email)

#     if not user:
#         return False

#     if verify_password(password, user.get("password_hash", "")):
#         st.session_state.auth = {
#             "logged_in": True,
#             "user_id": user["id"],
#         }
#         return True

#     return False

# def logout():
#     st.session_state.auth = {
#         "logged_in": False,
#         "user_id": None,
#     }

# def is_logged_in() -> bool:
#     ensure_session()
#     return st.session_state.auth.get("logged_in", False)

# def get_current_user() -> Optional[dict]:
#     ensure_session()
#     uid = st.session_state.auth.get("user_id")
#     if not uid:
#         return None

#     for u in get_users():
#         if u["id"] == uid:
#             return u
#     return None

# # ============================================================
# # RBAC
# # ============================================================
# PAGE_ROLE_MAP = {
#     "Dashboard": ["Admin", "Company", "Company_Aggregator", "Auditor"],
#     "Assessment (Level 1)": ["Company"],
#     "Assessment (Level 2)": ["Company", "Auditor"],
#     "Upload Document": ["Company"],
#     "OCR Processor": ["Auditor", "Admin"],
#     "Aggregator Overview": ["Company_Aggregator"],
#     "Question Editor (Admin)": ["Admin"],
#     "User Manager (Admin)": ["Admin"],
#     "Industry Clustering": ["Admin"],
#     "API Diagnostics": ["Admin"],
# }

# def require_roles_for_page(page_name: str, user: Optional[dict]) -> bool:
#     if page_name == "Login":
#         return True

#     required = PAGE_ROLE_MAP.get(page_name)
#     if not required:
#         return True

#     if not user:
#         return False

#     return any(r in user.get("roles", []) for r in required)

# # ============================================================
# # ADMIN HELPER
# # ============================================================
# def create_user(user_obj: dict) -> dict:
#     """
#     user_obj example:
#     {
#         "id": "...",
#         "email": "...",
#         "password_hash": "...",
#         "roles": [...],
#         "company_id": "...",
#         "created_at": "..."
#     }
#     """
#     db = load_json(USERS_PATH)
#     users = db.get("users", [])

#     if find_user_by_email(user_obj["email"]):
#         raise ValueError("Email already exists")

#     users.append(user_obj)
#     db["users"] = users
#     write_json(USERS_PATH, db)
#     return user_obj


# # streamlit_app/utils/auth_utils.py
# import os
# import streamlit as st
# from pathlib import Path
# from typing import Optional
# from streamlit_app.utils.data_access import load_json, write_json

# # bcrypt optional
# # try:
# #     import bcrypt
# #     _HAS_BCRYPT = True
# # except Exception:
# #     _HAS_BCRYPT = False
# _HAS_BCRYPT = False


# DB_ROOT = Path(os.getcwd()) / "backend" / "db" / "json_db"
# USERS_PATH = DB_ROOT / "users.json"

# def ensure_session():
#     if "auth" not in st.session_state:
#         st.session_state.auth = {"logged_in": False, "user_id": None}

# def get_users():
#     data = load_json(USERS_PATH)
#     return data.get("users", [])

# def find_user_by_email(email: str) -> Optional[dict]:
#     for u in get_users():
#         if u["email"].lower() == email.lower():
#             return u
#     return None

# def hash_password(plain: str) -> str:
#     if _HAS_BCRYPT:
#         return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()
#     return plain  # fallback (not secure)

# def verify_password(plain: str, hashed: str) -> bool:
#     if _HAS_BCRYPT:
#         try:
#             return bcrypt.checkpw(plain.encode(), hashed.encode())
#         except Exception:
#             return False
#     return plain == hashed

# def login(email: str, password: str) -> bool:
#     ensure_session()
#     user = find_user_by_email(email)
#     if not user:
#         return False
#     if verify_password(password, user.get("password_hash","")):
#         st.session_state.auth = {"logged_in": True, "user_id": user["id"]}
#         return True
#     return False

# def logout():
#     st.session_state.auth = {"logged_in": False, "user_id": None}

# def is_logged_in() -> bool:
#     ensure_session()
#     return st.session_state.auth.get("logged_in", False)

# def get_current_user() -> Optional[dict]:
#     ensure_session()
#     uid = st.session_state.auth.get("user_id")
#     if not uid:
#         return None
#     for u in get_users():
#         if u["id"] == uid:
#             return u
#     return None

# # RBAC mapping used by app.py
# PAGE_ROLE_MAP = {
#     "Dashboard": ["Admin", "Company", "Company_Aggregator", "Auditor"],
#     "Assessment (Level 1)": ["Company"],
#     "Assessment (Level 2)": ["Company", "Auditor"],
#     "Upload Document": ["Company"],
#     "OCR Processor": ["Auditor", "Admin"],
#     "Aggregator Overview": ["Company_Aggregator"],
#     "Question Editor (Admin)": ["Admin"],
#     "User Manager (Admin)": ["Admin"],
#     "Industry Clustering": ["Admin"],
#     "API Diagnostics": ["Admin"]
# }

# def require_roles_for_page(page_name: str, user: Optional[dict]) -> bool:
#     if page_name == "Login":
#         return True
#     required = PAGE_ROLE_MAP.get(page_name)
#     if not required:
#         return True
#     if not user:
#         return False
#     user_roles = user.get("roles", [])
#     return any(r in user_roles for r in required)

# # helper for admin user creation (used by admin page)
# def create_user(user_obj: dict) -> dict:
#     # user_obj: {id,email,password_hash,roles,company_id,created_at}
#     db = load_json(USERS_PATH)
#     users = db.get("users", [])
#     if find_user_by_email(user_obj["email"]):
#         raise ValueError("Email already exists")
#     users.append(user_obj)
#     db["users"] = users
#     write_json(USERS_PATH, db)
#     return user_obj
