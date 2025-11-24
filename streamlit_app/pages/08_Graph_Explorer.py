# streamlit_app/pages/08_Graph_Explorer.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in, get_current_user
from streamlit_app.utils.data_access import load_json, write_json
import networkx as nx
import json

DB_ROOT = Path(__file__).resolve().parents[2] / "backend" / "db" / "json_db"
GRAPH_PATH = DB_ROOT / "graph_store.json"

def run(st=st):
    st.header("Graph Explorer (pre-Neo4j)")
    if not is_logged_in():
        st.warning("Login required.")
        return
    user = get_current_user()
    graph_db = load_json(GRAPH_PATH).get("graph", {"nodes": [], "edges": []})
    nodes = graph_db.get("nodes", [])
    edges = graph_db.get("edges", [])

    st.subheader("Nodes")
    for n in nodes:
        st.write(f"- {n['id']} ({n.get('type')}) — {n.get('name','')}")
    st.subheader("Edges")
    for e in edges:
        st.write(f"- {e['source']} -[{e['relation']}]-> {e['target']}")

    st.markdown("---")
    st.subheader("Add node")
    with st.form("add_node"):
        nid = st.text_input("Node ID")
        ntype = st.selectbox("Type", ["Company","Document","Risk","Event","Entity"])
        name = st.text_input("Name")
        submit = st.form_submit_button("Add node")
        if submit:
            nodes.append({"id": nid, "type": ntype, "name": name})
            write_json(GRAPH_PATH, {"graph": {"nodes": nodes, "edges": edges}})
            st.success("Node added")

    st.subheader("Add edge")
    with st.form("add_edge"):
        src = st.text_input("Source ID")
        rel = st.text_input("Relation (HAS_DOCUMENT, INDICATES_RISK, etc.)")
        tgt = st.text_input("Target ID")
        submit_e = st.form_submit_button("Add edge")
        if submit_e:
            edges.append({"source": src, "target": tgt, "relation": rel})
            write_json(GRAPH_PATH, {"graph": {"nodes": nodes, "edges": edges}})
            st.success("Edge added")

    st.markdown("---")
    st.subheader("Visualize (NetworkX)")
    if st.button("Render Graph Preview"):
        try:
            G = nx.DiGraph()
            for n in nodes:
                G.add_node(n["id"], label=n.get("name"), type=n.get("type"))
            for e in edges:
                G.add_edge(e["source"], e["target"], relation=e.get("relation"))
            pos = nx.spring_layout(G, seed=42)
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8,6))
            nx.draw(G, pos, with_labels=True, node_size=800, arrowsize=20)
            st.pyplot(plt)
        except Exception as ex:
            st.error(f"Cannot render graph (missing libraries?): {ex}")
