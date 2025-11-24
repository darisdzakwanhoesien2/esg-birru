# streamlit_app/pages/12_Admin_Question_Editor.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json, write_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
QUEST_PATH = DB_ROOT / "questions.json"

def run(st=st):
    st.header("Question Editor (Admin)")
    if not is_logged_in():
        st.warning("Login required")
        return
    user = get_current_user()
    if "Admin" not in user.get("roles", []):
        st.error("Admin required")
        return
    db = load_json(QUEST_PATH)
    questions = db.get("questions", [])
    st.subheader("Existing")
    for q in questions:
        st.write(f"- {q['id']}: {q.get('text')}")
    st.markdown("---")
    with st.form("add_q"):
        qid = st.text_input("Question ID")
        text = st.text_area("Text")
        qtype = st.selectbox("Type", ["multiple_choice","essay"])
        choices = st.text_input("Choices (comma separated)")
        if st.form_submit_button("Add"):
            new = {"id": qid, "text": text, "type": qtype}
            if qtype=="multiple_choice":
                new["choices"] = [c.strip() for c in choices.split(",") if c.strip()]
            questions.append(new)
            write_json(QUEST_PATH, {"questions": questions})
            st.success("Added")
            st.json(new)
