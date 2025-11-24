# streamlit_app/pages/13_Admin_User_Manager.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user, create_user
from streamlit_app.utils.data_access import load_json, write_json
from datetime import datetime

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
USERS_PATH = DB_ROOT / "users.json"

def run(st=st):
    st.header("User Manager")
    if not is_logged_in():
        st.warning("Login required")
        return
    user = get_current_user()
    if "Admin" not in user.get("roles", []):
        st.error("Admin required")
        return
    users = load_json(USERS_PATH).get("users", [])
    st.subheader("Existing users")
    for u in users:
        st.write(f"- {u['id']} — {u['email']} — {u.get('roles')}")
    st.markdown("---")
    with st.form("create_user"):
        uid = st.text_input("User ID")
        email = st.text_input("Email")
        pw = st.text_input("Password")
        roles = st.text_input("Roles (comma separated)")
        cid = st.text_input("Company ID (optional)")
        if st.form_submit_button("Create"):
            hashed = pw  # auth_utils will accept plain or bcrypt as available
            new = {"id": uid, "email": email, "password_hash": hashed, "roles":[r.strip() for r in roles.split(",") if r.strip()], "company_id": cid or None, "created_at": datetime.utcnow().isoformat()+"Z"}
            try:
                create_user(new)
                st.success("User created")
                st.json(new)
            except Exception as e:
                st.error(str(e))
