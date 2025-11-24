# streamlit_app/pages/07_Media_Checker.py
import streamlit as st
from pathlib import Path
from datetime import datetime
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json, write_json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
MEDIA_PATH = DB_ROOT / "media_checks.json"

def simple_sentiment(text: str) -> float:
    pos = ["good","positive","award","reduce","improve","success","ambitious"]
    neg = ["violation","fined","investigation","scandal","emission","incident","accident","harm"]
    t = text.lower()
    score = sum(1 for w in pos if w in t) - sum(1 for w in neg if w in t)
    norm = score / max(len(t.split()),1)
    return round(max(min(norm,1.0), -1.0), 3)

def run(st=st):
    st.header("Media Checker")
    if not is_logged_in():
        st.warning("Login required")
        return
    user = get_current_user()
    st.subheader("Search media")
    company = st.text_input("Company ID (e.g., comp_001)")
    if st.button("Search"):
        db = load_json(MEDIA_PATH).get("media_checks", [])
        hits = [m for m in db if m["company_id"]==company]
        st.write(f"Found {len(hits)}")
        for h in hits:
            st.json(h)
    st.markdown("---")
    st.subheader("Add simulated media")
    with st.form("add_media"):
        comp = st.text_input("Company ID")
        platform = st.selectbox("Platform", ["news","twitter","linkedin","reddit"])
        url = st.text_input("Source URL")
        content = st.text_area("Content")
        submit = st.form_submit_button("Add media")
        if submit:
            if not comp or not content:
                st.error("company & content required")
            else:
                sent = simple_sentiment(content)
                db = load_json(MEDIA_PATH)
                entries = db.get("media_checks", [])
                media_id = f"media_{comp}_{int(datetime.utcnow().timestamp())}"
                obj = {
                    "media_id": media_id,
                    "company_id": comp,
                    "platform": platform,
                    "source_url": url or f"internal:{media_id}",
                    "content_text": content,
                    "sentiment": sent,
                    "stance": "positive" if sent>0.1 else ("negative" if sent<-0.1 else "neutral"),
                    "relevance_score": round(min(abs(sent)+0.5,1.0),3),
                    "verified_date": datetime.utcnow().isoformat()+"Z"
                }
                entries.append(obj)
                db["media_checks"] = entries
                write_json(MEDIA_PATH, db)
                st.success("Media added")
                st.json(obj)

