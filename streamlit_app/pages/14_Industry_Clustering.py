# streamlit_app/pages/14_Industry_Clustering.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.data_access import load_json, write_json
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
import os

DB_ROOT = Path(os.getcwd()) / "backend" / "db" / "json_db"
CLUSTERS_PATH = DB_ROOT / "clusters.json"
COMP_PATH = DB_ROOT / "companies.json"
L1_PATH = DB_ROOT / "assessments_level1.json"

def run(st=st):
    st.header("Industry Clustering (admin)")
    if not is_logged_in():
        st.warning("Login required")
        return
    user = get_current_user()
    if "Admin" not in user.get("roles", []):
        st.error("Admin required")
        return
    companies = load_json(COMP_PATH).get("companies", [])
    industry_map = {}
    for c in companies:
        industry_map.setdefault(c["industry"], []).append(c["id"])
    st.write(industry_map)
    if st.button("Run simple centroid clustering"):
        assessments = load_json(L1_PATH).get("assessments_level1", [])
        clusters = []
        for ind, comps in industry_map.items():
            scores = []
            for cid in comps:
                cs = [a.get("score",0) for a in assessments if a["company_id"]==cid]
                if cs:
                    scores.append(sum(cs)/len(cs))
            centroid = round(sum(scores)/len(scores),3) if scores else 0.0
            clusters.append({"industry":ind,"companies":comps,"centroid_score":centroid})
        write_json(CLUSTERS_PATH, {"industry_clusters": clusters})
        st.success("Clusters saved")
        st.json(clusters)
