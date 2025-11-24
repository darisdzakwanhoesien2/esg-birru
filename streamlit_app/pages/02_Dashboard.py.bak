# streamlit_app/pages/02_Dashboard.py
import streamlit as st
import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from streamlit_app.utils.auth_utils import get_current_user, is_logged_in
from streamlit_app.utils.data_access import load_json
from pathlib import Path

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"

def run(st=st):
    st.header("Dashboard")
    if not is_logged_in():
        st.warning("Please login to access the dashboard.")
        return

    user = get_current_user()
    st.subheader(f"Welcome, {user['email']}")
    st.markdown("#### Quick stats")

    # Show company-specific stats when a Company user
    if "Company" in user["roles"]:
        companies = load_json(DB_ROOT / "companies.json").get("companies", [])
        my_company = next((c for c in companies if c["id"] == user.get("company_id")), None)
        if my_company:
            st.metric("Company", my_company["name"])
            # load some aggregates
            assessments = load_json(DB_ROOT / "assessments_level1.json").get("assessments_level1", [])
            my_assess = [a for a in assessments if a["company_id"] == my_company["id"]]
            st.metric("Level1 assessments submitted", len(my_assess))
            st.markdown("**Certification status**")
            st.json(my_company.get("certification_status", {}))
        else:
            st.warning("No company found for your account.")

    # Admin view
    if "Admin" in user["roles"]:
        companies = load_json(DB_ROOT / "companies.json").get("companies", [])
        st.metric("Companies in DB", len(companies))
        users = load_json(DB_ROOT / "users.json").get("users", [])
        st.metric("Users", len(users))

    # Aggregator view
    if "Company_Aggregator" in user["roles"]:
        st.info("Aggregator: show grouped company status (placeholder)")

    st.markdown("---")
    st.markdown("Use the sidebar to navigate. Next steps: Submit Level 1 assessment, Upload evidence, Run OCR.")