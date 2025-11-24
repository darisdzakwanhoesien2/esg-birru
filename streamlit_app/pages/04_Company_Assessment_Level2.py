# streamlit_app/pages/04_Company_Assessment_Level2.py
import streamlit as st
from datetime import datetime
from pathlib import Path
import sys
import os

# Add the project root directory to the Python module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from streamlit_app.utils.auth_utils import get_current_user, is_logged_in
from streamlit_app.utils.data_access import load_json, write_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
L1_PATH = DB_ROOT / "assessments_level1.json"
L2_PATH = DB_ROOT / "assessments_level2.json"
DOCS_PATH = DB_ROOT / "documents.json"
OCR_PATH = DB_ROOT / "ocr_results.json"

def run(st=st):
    st.header("Company Assessment — Level 2 (Evidence Verification)")
    if not is_logged_in():
        st.warning("Please login.")
        return
    user = get_current_user()
    if "Company" not in user["roles"] and "Auditor" not in user["roles"] and "Admin" not in user["roles"]:
        st.error("Only Company/Auditor/Admin can access level 2.")
        return

    st.markdown("### Create new Level 2 assessment (Company step)")
    if "Company" in user["roles"]:
        l1_db = load_json(L1_PATH).get("assessments_level1", [])
        my_l1 = [a for a in l1_db if a["company_id"] == user["company_id"]]
        if not my_l1:
            st.info("No Level 1 assessments found for your company. Complete Level 1 first.")
        else:
            sel = st.selectbox("Select Level 1 to attach evidence to", [a["assessment_id"] for a in my_l1])
            uploaded = st.file_uploader("Upload evidence document (pdf/jpg/png)", type=["pdf", "png", "jpg", "jpeg"])
            if st.button("Create Level 2 Evidence Record"):
                if not uploaded:
                    st.error("Upload file first.")
                else:
                    # delegate to existing Document Uploader flow by writing entry
                    docs_db = load_json(DOCS_PATH)
                    entries = docs_db.get("documents", [])
                    doc_id = f"doc_{user['company_id']}_{int(datetime.utcnow().timestamp())}"
                    company_storage = Path(__file__).resolve().parents[2].parent / "storage" / "uploads" / user["company_id"]
                    company_storage.mkdir(parents=True, exist_ok=True)
                    filename = f"{doc_id}_{uploaded.name}"
                    dest = company_storage / filename
                    with open(dest, "wb") as f:
                        f.write(uploaded.getbuffer())
                    doc_obj = {
                        "doc_id": doc_id,
                        "company_id": user["company_id"],
                        "assessment_id": sel,
                        "filename": uploaded.name,
                        "file_path": str(dest),
                        "ocr_status": "pending",
                        "ocr_result_id": None,
                        "uploaded_at": datetime.utcnow().isoformat() + "Z"
                    }
                    entries.append(doc_obj)
                    docs_db["documents"] = entries
                    write_json(DOCS_PATH, docs_db)
                    st.success("Evidence uploaded and linked to Level 1 assessment.")
                    st.json(doc_obj)

    st.markdown("---")
    st.markdown("### Auditor actions")
    if "Auditor" in user["roles"] or "Admin" in user["roles"]:
        st.write("Review pending Level 2 verifications")
        docs_db = load_json(DOCS_PATH).get("documents", [])
        pending_docs = [d for d in docs_db if d.get("ocr_status") in (None, "pending", "processed")]
        if not pending_docs:
            st.info("No documents available.")
            return
        sel = st.selectbox("Select document to review", [f"{d['doc_id']} — {Path(d['file_path']).name}" for d in pending_docs])
        doc_id = sel.split(" — ")[0]
        doc = next(d for d in pending_docs if d["doc_id"] == doc_id)
        st.write("Document metadata:")
        st.json(doc)
        # show OCR result if exists
        ocr_db = load_json(OCR_PATH).get("ocr_results", [])
        ocr = next((o for o in ocr_db if o["doc_id"] == doc_id), None)
        if ocr:
            st.markdown("**OCR result:**")
            st.write(ocr.get("extracted_text","(empty)"))
            st.markdown(f"Confidence: {ocr.get('confidence_score')}")
        else:
            st.info("No OCR result available for this doc.")

        st.markdown("Verification:")
        decision = st.selectbox("Decision", ["approve", "flag", "require_more_evidence"])
        comments = st.text_area("Auditor comments")
        if st.button("Apply verification"):
            # append or create level2 assessment entry
            l2_db = load_json(L2_PATH)
            entries = l2_db.get("level2_assessments", [])
            existing = next((e for e in entries if e.get("assessment_id") == f"assess_{doc['company_id']}_L2_{doc['assessment_id']}"), None)
            new_obj = {
                "assessment_id": f"assess_{doc['company_id']}_L2_{doc['assessment_id']}_{int(datetime.utcnow().timestamp())}",
                "company_id": doc["company_id"],
                "level": 2,
                "linked_level1": doc["assessment_id"],
                "evidence_documents": [doc["doc_id"]],
                "verification_steps": [
                    {"step": "auditor_review", "status": decision, "auditor_id": user["id"], "comments": comments}
                ],
                "final_score": 0.0,
                "explainability": {"llm_summary": "", "graph_paths": []},
                "completed_at": datetime.utcnow().isoformat() + "Z"
            }
            entries.append(new_obj)
            l2_db["level2_assessments"] = entries
            write_json(L2_PATH, l2_db)
            st.success("Verification record created.")
            st.json(new_obj)