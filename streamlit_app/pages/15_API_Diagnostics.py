# streamlit_app/pages/15_API_Diagnostics.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json
import os

DB_ROOT = Path(os.getcwd()) / "backend" / "db" / "json_db"
FILES = ["users.json","companies.json","assessments_level1.json","assessments_level2.json","documents.json","ocr_results.json","media_checks.json","graph_store.json","clusters.json","roles_permissions.json","certification_rules.json"]

def run(st=st):
    st.header("API Diagnostics")
    if not is_logged_in():
        st.warning("Login required")
        return
    user = get_current_user()
    if "Admin" not in user.get("roles", []):
        st.error("Admin required")
        return
    for fname in FILES:
        path = DB_ROOT / fname
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        st.write(f"- {fname}: exists={exists}, size={size}")
        if exists:
            data = load_json(path)
            if isinstance(data, dict):
                st.write("  keys:", list(data.keys()))
