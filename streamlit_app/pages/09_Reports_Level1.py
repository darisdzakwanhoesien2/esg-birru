# streamlit_app/pages/09_Reports_Level1.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
L1_PATH = DB_ROOT / "assessments_level1.json"
COMP_PATH = DB_ROOT / "companies.json"
TEMPLATES = DB_ROOT / "report_templates.json"

def run(st=st):
    st.header("Level 1 Reports")
    if not is_logged_in():
        st.warning("Login required.")
        return
    user = get_current_user()
    st.markdown("Generate Level 1 report for a company")

    companies = load_json(COMP_PATH).get("companies", [])
    comp_map = {c["id"]: c for c in companies}
    sel = st.selectbox("Company", ["--select--"] + [c["id"] for c in companies])
    if sel and sel != "--select--":
        # collect assessments
        l1_db = load_json(L1_PATH).get("assessments_level1", [])
        my = [a for a in l1_db if a["company_id"] == sel]
        st.markdown("### Assessment items")
        st.write(f"Found {len(my)} L1 assessments")
        for a in my:
            st.json(a)
        # basic report assembly
        tmpl = load_json(TEMPLATES).get("report_templates", {}).get("level1", {})
        report = {
            "company": comp_map[sel],
            "generated_at": st.session_state.get("now", "unknown"),
            "sections": tmpl.get("sections", []),
            "assessments": my
        }
        if st.button("Export report JSON"):
            st.download_button("Download JSON", data=str(report), file_name=f"report_l1_{sel}.json")
        st.markdown("---")
        st.markdown("Report preview")
        st.json(report)
