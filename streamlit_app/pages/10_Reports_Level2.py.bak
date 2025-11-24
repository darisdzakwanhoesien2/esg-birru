# streamlit_app/pages/10_Reports_Level2.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in
from streamlit_app.utils.data_access import load_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
L2_PATH = DB_ROOT / "assessments_level2.json"
COMP_PATH = DB_ROOT / "companies.json"
CERT = DB_ROOT / "certification_rules.json"

def run(st=st):
    st.header("Level 2 Reports & Recommendation")
    if not is_logged_in():
        st.warning("Login required")
        return
    companies = load_json(COMP_PATH).get("companies", [])
    sel = st.selectbox("Company", ["--select--"] + [c["id"] for c in companies])
    if sel and sel != "--select--":
        l2 = load_json(L2_PATH).get("level2_assessments", [])
        entries = [e for e in l2 if e["company_id"]==sel]
        st.write(f"Found {len(entries)} L2 entries")
        for e in entries:
            st.json(e)
        # simple scoring
        if entries:
            avg = sum(e.get("final_score",0.0) for e in entries)/len(entries)
            st.write("Avg L2 score:", round(avg,3))
            rules = load_json(CERT).get("scoring_rules", {})
            threshold = rules.get("level2",{}).get("passing_threshold", 0.7)
            if avg >= threshold:
                st.success("Recommendation: Certified (subject to L1)")
            elif avg >= threshold - 0.1:
                st.warning("Recommendation: Conditional Certification")
            else:
                st.error("Recommendation: Not Certified")
        else:
            st.info("No L2 data.")
