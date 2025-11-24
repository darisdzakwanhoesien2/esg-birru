# streamlit_app/pages/05_Document_Uploader.py
import streamlit as st
from pathlib import Path
from datetime import datetime
from streamlit_app.utils.auth_utils import get_current_user, is_logged_in
from streamlit_app.utils.data_access import load_json, write_json
import uuid

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
DOCS_PATH = DB_ROOT / "documents.json"
STORAGE_ROOT = Path(__file__).resolve().parents[2].parent / "storage" / "uploads"

def run(st=st):
    st.header("Upload Evidence Document")
    if not is_logged_in():
        st.warning("Please login first.")
        return
    user = get_current_user()
    if "Company" not in user.get("roles", []):
        st.error("Only Company users can upload documents.")
        return

    st.markdown("Upload PDF or image as evidence for an assessment.")
    uploaded = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])
    assessment_id = st.text_input("Assessment ID (optional) — link to assessment", value="")
    if st.button("Upload"):
        if not uploaded:
            st.error("Choose a file first.")
            return
        # Save file
        company_dir = STORAGE_ROOT / user["company_id"]
        company_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4().hex}_{uploaded.name}"
        dest = company_dir / filename
        with open(dest, "wb") as f:
            f.write(uploaded.getbuffer())

        # Update documents.json
        db = load_json(DOCS_PATH)
        entries = db.get("documents", [])
        doc_id = f"doc_{user['company_id']}_{int(datetime.utcnow().timestamp())}"
        doc_obj = {
            "doc_id": doc_id,
            "company_id": user["company_id"],
            "assessment_id": assessment_id or None,
            "filename": uploaded.name,
            "file_path": str(dest),
            "ocr_status": "pending",
            "ocr_result_id": None,
            "uploaded_at": datetime.utcnow().isoformat() + "Z"
        }
        entries.append(doc_obj)
        db["documents"] = entries
        write_json(DOCS_PATH, db)

        st.success("File uploaded.")
        st.json(doc_obj)
