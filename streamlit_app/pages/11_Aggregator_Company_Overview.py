# streamlit_app/pages/11_Aggregator_Company_Overview.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json
import os

DB_ROOT = Path(os.getcwd()) / "backend" / "db" / "json_db"

def run(st=st):
    st.header("Aggregator Overview")
    if not is_logged_in():
        st.warning("Login required")
        return
    user = get_current_user()
    if "Company_Aggregator" not in user.get("roles", []):
        st.error("Aggregator role required")
        return
    comps = load_json(DB_ROOT / "companies.json").get("companies", [])
    for c in comps:
        st.markdown(f"**{c['id']}** — {c['name']} ({c['industry']})")
        st.json(c.get("certification_status", {}))
