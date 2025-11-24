# streamlit_app/pages/04_Company_Assessment_Level2.py
import streamlit as st
from pathlib import Path
from datetime import datetime
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json, write_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
DOCS_PATH = DB_ROOT / "documents.json"
L2_PATH = DB_ROOT / "assessments_level2.json"
OCR_PATH = DB_ROOT / "ocr_results.json"

def run(st=st):
    st.header("Level 2 — Evidence Verification")
    if not is_logged_in():
        st.warning("Login required.")
        return
    user = get_current_user()
    if "Company" in user.get("roles", []):
        st.subheader("Upload evidence for a Level 1 assessment (Company)")
        l1_path = DB_ROOT / "assessments_level1.json"
        l1_db = load_json(l1_path).get("assessments_level1", [])
        my_l1 = [a for a in l1_db if a["company_id"] == user["company_id"]]
        if not my_l1:
            st.info("No Level 1 entries found. Complete Level 1 first.")
        else:
            sel = st.selectbox("Select Level 1 assessment", [a["assessment_id"] for a in my_l1])
            uploaded = st.file_uploader("Evidence file (pdf/jpg/png)", type=["pdf","png","jpg","jpeg"])
            if st.button("Upload evidence"):
                if not uploaded:
                    st.error("Choose file first")
                else:
                    company_dir = Path(__file__).resolve().parents[2].parent / "storage" / "uploads" / user["company_id"]
                    company_dir.mkdir(parents=True, exist_ok=True)
                    fname = f"{int(datetime.utcnow().timestamp())}_{uploaded.name}"
                    dest = company_dir / fname
                    with open(dest, "wb") as f:
                        f.write(uploaded.getbuffer())
                    docs = load_json(DOCS_PATH).get("documents", [])
                    doc_id = f"doc_{user['company_id']}_{int(datetime.utcnow().timestamp())}"
                    obj = {
                        "doc_id": doc_id,
                        "company_id": user["company_id"],
                        "assessment_id": sel,
                        "filename": uploaded.name,
                        "file_path": str(dest),
                        "ocr_status": "pending",
                        "ocr_result_id": None,
                        "uploaded_at": datetime.utcnow().isoformat()+"Z"
                    }
                    docs.append(obj)
                    write_json(DOCS_PATH, {"documents": docs})
                    st.success("Evidence uploaded")
                    st.json(obj)

    if "Auditor" in user.get("roles", []) or "Admin" in user.get("roles", []):
        st.subheader("Auditor: review pending evidence")
        docs = load_json(DOCS_PATH).get("documents", [])
        pending = [d for d in docs if d.get("ocr_status") in (None, "pending", "processed")]
        if not pending:
            st.info("No pending docs")
            return
        sel = st.selectbox("Pending document", [f"{d['doc_id']} — {Path(d['file_path']).name}" for d in pending])
        doc_id = sel.split(" — ")[0]
        doc = next(d for d in pending if d["doc_id"]==doc_id)
        st.json(doc)
        # show OCR if exists
        ocr_db = load_json(OCR_PATH).get("ocr_results", [])
        ocr = next((o for o in ocr_db if o["doc_id"]==doc_id), None)
        if ocr:
            st.markdown("**OCR**")
            st.write(ocr.get("extracted_text",""))
            st.write("Confidence:", ocr.get("confidence_score"))
        decision = st.selectbox("Decision", ["approve","flag","require_more_evidence"])
        comments = st.text_area("Comments")
        if st.button("Apply decision"):
            l2_db = load_json(L2_PATH)
            entries = l2_db.get("level2_assessments", [])
            rec = {
                "assessment_id": f"assess_{doc['company_id']}_L2_{int(datetime.utcnow().timestamp())}",
                "company_id": doc["company_id"],
                "level": 2,
                "linked_level1": doc["assessment_id"],
                "evidence_documents": [doc["doc_id"]],
                "verification_steps": [
                    {"step":"auditor_review","status":decision,"auditor_id":user["id"],"comments":comments}
                ],
                "final_score": 0.0,
                "explainability": {"llm_summary":"","graph_paths":[]},
                "completed_at": datetime.utcnow().isoformat()+"Z"
            }
            entries.append(rec)
            l2_db["level2_assessments"] = entries
            write_json(L2_PATH, l2_db)
            st.success("Level 2 record created")
            st.json(rec)
