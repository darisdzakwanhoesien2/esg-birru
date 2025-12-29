# streamlit_app/pages/06_OCR_Processor.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json, write_json
from datetime import datetime
import pytesseract  # optional; placeholder, may not be installed
from PIL import Image
import os

DB_ROOT = Path(os.getcwd()) / "backend" / "db" / "json_db"
DOCS_PATH = DB_ROOT / "documents.json"
OCR_PATH = DB_ROOT / "ocr_results.json"

def simple_ocr_text(filepath: str) -> (str, float):
    """
    Placeholder OCR function.
    If pillow + pytesseract installed, run real OCR on images.
    For PDF, you will need pdf->image conversion (not included).
    Returns (text, confidence)
    """
    try:
        # Attempt to treat file as image
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
        # crude confidence
        conf = 0.85 if len(text) > 20 else 0.45
        return text, conf
    except Exception:
        # fallback simulated extraction
        return "SIMULATED OCR TEXT: extracted content snippet...", 0.6

def run(st=st):
    st.header("OCR Processor")
    if not is_logged_in():
        st.warning("Please login to continue.")
        return
    user = get_current_user()
    if "Auditor" not in user.get("roles", []) and "Admin" not in user.get("roles", []):
        st.error("Only Auditor or Admin can run OCR processing.")
        return

    st.markdown("Select a pending document to process OCR for.")
    docs_db = load_json(DOCS_PATH).get("documents", [])
    pending = [d for d in docs_db if d.get("ocr_status") in (None, "pending")]
    if not pending:
        st.info("No pending documents.")
        return

    sel = st.selectbox("Pending documents", [f"{d['doc_id']} — {Path(d['file_path']).name}" for d in pending])
    if st.button("Run OCR"):
        # find doc
        doc_id = sel.split(" — ")[0]
        doc = next(d for d in pending if d["doc_id"] == doc_id)
        filepath = doc["file_path"]
        text, conf = simple_ocr_text(filepath)
        # write to OCR DB
        ocr_db = load_json(OCR_PATH)
        entries = ocr_db.get("ocr_results", [])
        ocr_id = f"ocr_{doc_id}_{int(datetime.utcnow().timestamp())}"
        ocr_obj = {
            "ocr_id": ocr_id,
            "doc_id": doc_id,
            "extracted_text": text,
            "named_entities": [],
            "confidence_score": round(conf, 3),
            "processed_at": datetime.utcnow().isoformat() + "Z"
        }
        entries.append(ocr_obj)
        ocr_db["ocr_results"] = entries
        write_json(OCR_PATH, ocr_db)
        # update document record
        for d in docs_db:
            if d["doc_id"] == doc_id:
                d["ocr_status"] = "processed"
                d["ocr_result_id"] = ocr_id
        write_json(DOCS_PATH, {"documents": docs_db})

        st.success("OCR completed.")
        st.json(ocr_obj)
