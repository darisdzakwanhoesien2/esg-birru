# streamlit_app/pages/10_Reports_Level2.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in
from streamlit_app.utils.data_access import load_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
L2_PATH = DB_ROOT / "assessments_level2.json"
COMP_PATH = DB_ROOT / "companies.json"
TEMPLATES = DB_ROOT / "report_templates.json"
CERT_RULES = DB_ROOT / "certification_rules.json"

def run(st=st):
    st.header("Level 2 Reports & Certification Recommendation")
    if not is_logged_in():
        st.warning("Login required.")
        return

    companies = load_json(COMP_PATH).get("companies", [])
    sel = st.selectbox("Company", ["--select--"] + [c["id"] for c in companies])
    if sel and sel != "--select--":
        l2_db = load_json(L2_PATH).get("level2_assessments", [])
        entries = [e for e in l2_db if e["company_id"] == sel]
        st.write(f"Found {len(entries)} L2 assessments")
        for e in entries:
            st.json(e)

        # simple recommendation: use certification_rules
        rules = load_json(CERT_RULES).get("scoring_rules", {})
        # derive simple aggregated scores
        avg_score = None
        if entries:
            avg_score = sum(e.get("final_score", 0.0) for e in entries) / len(entries)
        st.markdown("### Recommendation")
        if avg_score is None:
            st.info("No level 2 data to recommend certification.")
        else:
            st.write("Average L2 score:", round(avg_score,3))
            # naive risk lookups not implemented here
            if avg_score >= rules.get("level2", {}).get("passing_threshold", 0.7):
                st.success("Recommendation: PASS — Certified (subject to Level1 check)")
            elif avg_score >= 0.6:
                st.warning("Recommendation: Conditional Certification")
            else:
                st.error("Recommendation: NOT Certified")
