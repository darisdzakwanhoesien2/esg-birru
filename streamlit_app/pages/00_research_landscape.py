import json
import streamlit as st
import plotly.graph_objects as go

st.header("🔗 Research Framework Sankey Diagram")

# -------------------------------------------------
# Load research framework JSON
# -------------------------------------------------
with open("data/research_framework.json") as f:
    framework = json.load(f)

# -------------------------------------------------
# Helper functions (ROBUST)
# -------------------------------------------------
def get_label(item):
    if isinstance(item, dict):
        return (
            item.get("label")
            or item.get("title")
            or item.get("text")
            or item.get("id")
        )
    return str(item)


def get_description(item):
    if isinstance(item, dict):
        return (
            item.get("description")
            or item.get("question")
            or item.get("text")
            or ""
        )
    return ""

# -------------------------------------------------
# Normalize metrics (handles dict or list)
# -------------------------------------------------
metrics_items = []
metrics = framework.get("metrics", {})

if isinstance(metrics, dict):
    for _, metric_list in metrics.items():
        for m in metric_list:
            metrics_items.append({"id": m})
elif isinstance(metrics, list):
    metrics_items = metrics

# =================================================
# SECTION 1 — LIST FRAMEWORK DATA
# =================================================

with st.expander("📘 Research Questions", expanded=True):
    for rq in framework.get("research_questions", []):
        st.markdown(f"**{get_label(rq)}**  \n{get_description(rq)}")

with st.expander("🎯 Research Objectives"):
    for obj in framework.get("objectives", []):
        st.markdown(f"**{get_label(obj)}**  \n{get_description(obj)}")

with st.expander("🧪 Methodology"):
    for m in framework.get("methodology", []):
        st.markdown(f"**{get_label(m)}**  \n{get_description(m)}")

with st.expander("🧠 Hypotheses"):
    for h in framework.get("hypotheses", []):
        st.markdown(f"**{get_label(h)}**  \n{get_description(h)}")

with st.expander("📊 Evaluation Metrics"):
    for metric in metrics_items:
        st.markdown(f"**{get_label(metric)}**")

st.divider()

# =================================================
# SECTION 2 — SANKEY DIAGRAM
# =================================================

st.subheader("🔄 Research Logic Flow")

nodes = []
node_index = {}

def add_node(node_id, label):
    if node_id not in node_index:
        node_index[node_id] = len(nodes)
        nodes.append(label)

# Register nodes
for section in ["research_questions", "objectives", "methodology", "hypotheses"]:
    for item in framework.get(section, []):
        add_node(item["id"], get_label(item))

for metric in metrics_items:
    add_node(metric["id"], get_label(metric))

# Build links
sources, targets, values = [], [], []

for link in framework.get("connections", []):
    sources.append(node_index[link["source"]])
    targets.append(node_index[link["target"]])
    values.append(1)

# Create Sankey diagram
fig = go.Figure(
    go.Sankey(
        node=dict(
            pad=18,
            thickness=20,
            label=nodes
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )
)

fig.update_layout(
    title="ESG Research Framework: Questions → Objectives → Methods → Hypotheses → Metrics",
    font_size=12
)

st.plotly_chart(fig, use_container_width=True)
