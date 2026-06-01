# streamlit_app/pages/08_Graph_Explorer.py
import streamlit as st
from pathlib import Path
from streamlit_app.utils.auth_utils import is_logged_in
from streamlit_app.utils.data_access import load_json, write_json
from streamlit_app.utils.paths import get_db_root
import networkx as nx
import matplotlib.pyplot as plt

# Avoid `os.getcwd()` so this works reliably across different launch contexts.
DB_ROOT = get_db_root()
GRAPH_PATH = DB_ROOT / "graph_store.json"

def run(st=st):
    st.header("Graph Explorer")
    if not is_logged_in():
        st.warning("Login required")
        return
    graph_db = load_json(GRAPH_PATH).get("graph", {"nodes": [], "edges": []})
    nodes = graph_db.get("nodes", [])
    edges = graph_db.get("edges", [])
    st.subheader("Nodes")
    for n in nodes:
        st.write(f"- {n['id']} ({n.get('type')}) {n.get('name','')}")
    st.subheader("Edges")
    for e in edges:
        st.write(f"- {e['source']} -[{e['relation']}]-> {e['target']}")

    st.markdown("---")
    with st.form("add_node"):
        nid = st.text_input("Node ID")
        ntype = st.selectbox("Type", ["Company","Document","Risk","Event","Entity"])
        name = st.text_input("Name")
        if st.form_submit_button("Add node"):
            if not nid.strip():
                st.error("Node ID is required.")
                st.stop()
            nodes.append({"id": nid, "type": ntype, "name": name})
            write_json(GRAPH_PATH, {"graph": {"nodes": nodes, "edges": edges}})
            st.success("Node added")
    with st.form("add_edge"):
        src = st.text_input("Source ID", key="src")
        rel = st.text_input("Relation", key="rel")
        tgt = st.text_input("Target ID", key="tgt")
        if st.form_submit_button("Add edge"):
            if not src.strip() or not tgt.strip() or not rel.strip():
                st.error("Source, relation, and target are required.")
                st.stop()
            edges.append({"source": src, "target": tgt, "relation": rel})
            write_json(GRAPH_PATH, {"graph": {"nodes": nodes, "edges": edges}})
            st.success("Edge added")

    if st.button("Render preview"):
        try:
            # Convert the stored node/edge JSON into a NetworkX directed graph,
            # then render it with a deterministic layout (seeded) for consistent previews.
            G = nx.DiGraph()
            for n in nodes:
                G.add_node(n["id"], label=n.get("name"))
            for e in edges:
                G.add_edge(e["source"], e["target"], relation=e.get("relation"))
            pos = nx.spring_layout(G, seed=42)
            plt.figure(figsize=(8,6))
            nx.draw(G, pos, with_labels=True, node_size=700, arrowsize=20)
            st.pyplot(plt)
        except Exception as ex:
            st.error(f"Could not render graph: {ex}")
