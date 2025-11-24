# streamlit_app/pages/12_Admin_Question_Editor.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json, write_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
QUESTIONS_PATH = DB_ROOT / "questions.json"

def run(st=st):
    st.header("Admin — Question Editor")
    if not is_logged_in():
        st.warning("Login required.")
        return
    user = get_current_user()
    if "Admin" not in user.get("roles", []):
        st.error("Admin role required.")
        return

    db = load_json(QUESTIONS_PATH)
    questions = db.get("questions", [])
    st.subheader("Existing Questions")
    for q in questions:
        st.write(f"- {q['id']}: {q.get('text')} ({q.get('type')})")

    st.markdown("---")
    st.subheader("Add new question")
    with st.form("q_form"):
        qid = st.text_input("Question ID")
        text = st.text_area("Question text")
        qtype = st.selectbox("Type", ["multiple_choice","essay"])
        choices = st.text_input("Choices (comma separated, only for multiple_choice)")
        submit = st.form_submit_button("Add question")
        if submit:
            new = {"id": qid, "text": text, "type": qtype}
            if qtype == "multiple_choice":
                new["choices"] = [c.strip() for c in choices.split(",") if c.strip()]
            questions.append(new)
            db["questions"] = questions
            write_json(QUESTIONS_PATH, db)
            st.success("Question added")
            st.json(new)
