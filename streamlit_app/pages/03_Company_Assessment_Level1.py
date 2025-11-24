# streamlit_app/pages/03_Company_Assessment_Level1.py
import streamlit as st
from datetime import datetime
from pathlib import Path
from utils.auth_utils import get_current_user, is_logged_in
from utils.data_access import load_json, write_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
ASSESS_PATH = DB_ROOT / "assessments_level1.json"

# Example question schema (in production, load from questions file)
QUESTIONS = [
    {"id": "Q01", "text": "Does your company have an ESG policy?", "type": "multiple_choice", "choices": ["Yes", "No"]},
    {"id": "Q02", "text": "Provide your carbon reduction target (essay).", "type": "essay"}
]

def run(st=st):
    st.header("Company Assessment — Level 1")
    if not is_logged_in():
        st.warning("Please login first.")
        return
    user = get_current_user()
    if "Company" not in user.get("roles", []):
        st.error("Only Company users may submit Level 1 assessment.")
        return

    st.write("Please answer the following assessment questions:")
    answers = {}
    with st.form("l1_form"):
        for q in QUESTIONS:
            if q["type"] == "multiple_choice":
                answers[q["id"]] = st.radio(q["text"], q["choices"], key=q["id"])
            elif q["type"] == "essay":
                answers[q["id"]] = st.text_area(q["text"], key=q["id"])
        submitted = st.form_submit_button("Submit Level 1 Assessment")
        if submitted:
            # naive scoring: simple heuristics for demo
            score = 0
            if answers.get("Q01") == "Yes":
                score += 1.0
            if answers.get("Q02") and len(answers.get("Q02")) > 10:
                score += 0.9
            score = score / 2.0  # normalize 0..1

            # load existing assessments
            db = load_json(ASSESS_PATH)
            entries = db.get("assessments_level1", [])
            new = {
                "assessment_id": f"assess_{user['company_id']}_L1_{int(datetime.utcnow().timestamp())}",
                "company_id": user["company_id"],
                "level": 1,
                "submitted_at": datetime.utcnow().isoformat() + "Z",
                "answers": answers,
                "score": round(score, 3),
                "linked_documents": []
            }
            entries.append(new)
            db["assessments_level1"] = entries
            write_json(ASSESS_PATH, db)
            st.success("Assessment submitted.")
            st.json(new)
