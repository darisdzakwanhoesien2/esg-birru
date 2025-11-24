# streamlit_app/pages/13_Admin_User_Manager.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.data_access import load_json, write_json
from streamlit_app.utils.auth_utils import get_users
from streamlit_app.utils.auth_utils import find_user_by_email
import bcrypt
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
USERS_PATH = DB_ROOT / "users.json"

def hash_password(pw: str) -> str:
    try:
        return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
    except Exception:
        # fallback (plain) - not secure
        return pw

def run(st=st):
    st.header("Admin — User Manager")
    if not is_logged_in():
        st.warning("Login required.")
        return
    user = get_current_user()
    if "Admin" not in user.get("roles", []):
        st.error("Admin role required.")
        return

    db = load_json(USERS_PATH)
    users = db.get("users", [])
    st.subheader("Existing users")
    for u in users:
        st.write(f"- {u['id']} — {u['email']} — roles: {u.get('roles')}")

    st.markdown("---")
    st.subheader("Create user")
    with st.form("create_user"):
        uid = st.text_input("User ID")
        email = st.text_input("Email")
        pw = st.text_input("Password")
        roles = st.text_input("Roles (comma separated)")
        cid = st.text_input("Company ID (optional)")
        submit = st.form_submit_button("Create user")
        if submit:
            if find_user_by_email(email):
                st.error("Email already exists")
            else:
                h = hash_password(pw)
                obj = {"id": uid, "email": email, "password_hash": h, "roles": [r.strip() for r in roles.split(",") if r.strip()], "company_id": cid or None, "created_at": st.session_state.get("now","")}
                users.append(obj)
                db["users"] = users
                write_json(USERS_PATH, db)
                st.success("User created")
                st.json(obj)
