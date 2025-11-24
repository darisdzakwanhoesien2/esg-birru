# streamlit_app/pages/09_Reports_Level1.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
L1_PATH = DB_ROOT / "assessments_level1.json"
COMP_PATH = DB_ROOT / "companies.json"
TEMPLATE_PATH = DB_ROOT / "report_templates.json"

def run(st=st):
    st.header("Level 1 Reports")
    if not is_logged_in():
        st.warning("Login required")
        return
    companies = load_json(COMP_PATH).get("companies", [])
    sel = st.selectbox("Company", ["--select--"] + [c["id"] for c in companies])
    if sel and sel != "--select--":
        l1 = load_json(L1_PATH).get("assessments_level1", [])
        res = [a for a in l1 if a["company_id"]==sel]
        st.write(f"Found {len(res)} assessments")
        for r in res:
            st.json(r)
        # assemble report
        tmpl = load_json(TEMPLATE_PATH).get("report_templates", {}).get("level1", {})
        report = {"company_id": sel, "assessments": res, "sections": tmpl.get("sections", [])}
        if st.button("Download report JSON"):
            st.download_button("report", data=str(report), file_name=f"report_l1_{sel}.json")
        st.markdown("---")
        st.json(report)
