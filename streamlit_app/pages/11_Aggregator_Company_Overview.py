# streamlit_app/pages/11_Aggregator_Company_Overview.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"

def run(st=st):
    st.header("Aggregator — Company Overview")
    if not is_logged_in():
        st.warning("Login required.")
        return
    user = get_current_user()
    if "Company_Aggregator" not in user.get("roles", []):
        st.error("Only aggregator users may access this view.")
        return

    companies = load_json(DB_ROOT / "companies.json").get("companies", [])
    st.write(f"Companies ({len(companies)}):")
    for c in companies:
        st.write("---")
        st.markdown(f"**{c['id']}** — {c['name']} ({c['industry']})")
        st.json(c.get("certification_status", {}))
