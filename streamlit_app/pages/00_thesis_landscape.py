import streamlit as st
from pathlib import Path

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------
st.set_page_config(
    page_title="ESG Dashboard — Navigation & Documentation",
    layout="wide"
)

st.title("📊 ESG Sentence-Level Analytics Dashboard")
st.caption(
    "This dashboard provides an auditable, ontology-aware, sentence-level analysis "
    "of ESG disclosures across documents, models, and providers."
)

# -------------------------------------------------------
# Project Context
# -------------------------------------------------------
st.markdown("""
### 🎯 What this dashboard is for

This system is designed to:

- Parse **LLM-generated ESG annotations** from raw document text
- Normalize them using **auditable ESG ontologies**
- Compare **multiple models and providers**
- Inspect **sentiment, tone, aspect, and grounding**
- Support **research, assurance, and regulatory workflows**

All analysis is **sentence-level** and **traceable back to source text**.
""")

st.markdown("---")

# -------------------------------------------------------
# How to Navigate
# -------------------------------------------------------
st.markdown("""
## 🧭 How to navigate

Use the **left sidebar** to switch between pages.  
Each page focuses on a *specific stage* of the ESG analysis pipeline.

Below is a guided explanation of every page.
""")

# -------------------------------------------------------
# PAGE DOCUMENTATION
# -------------------------------------------------------

def page_doc(title, file, purpose, inputs, outputs, when_to_use):
    with st.expander(f"📄 {title}", expanded=False):
        st.markdown(f"""
**📁 File:** `{file}`

**🎯 Purpose**  
{purpose}

**📥 Inputs**  
{inputs}

**📤 Outputs / Visuals**  
{outputs}

**🧠 When to use this page**  
{when_to_use}
""")

# -------------------------------------------------------
# Core Pages
# -------------------------------------------------------

st.subheader("🧩 Core Analysis Pages")

page_doc(
    title="Parsed ESG Sentence Dashboard",
    file="app.py (this page)",
    purpose="""
Acts as the **entry point and documentation hub** for the entire ESG dashboard.
Provides context, navigation guidance, and analytical structure.
""",
    inputs="""
- No direct data processing
- Relies on downstream pages for computation
""",
    outputs="""
- Conceptual overview
- Page-by-page documentation
""",
    when_to_use="""
Start here if you are new to the dashboard or onboarding a new reviewer.
"""
)

page_doc(
    title="Distributions",
    file="Data Distribution.py / Data_New_Distribution.py",
    purpose="""
Explore **global distributions** of aspect categories, sentiment, and tone.
Useful for sanity checks and dataset-level patterns.
""",
    inputs="""
- `data_output.csv` or `output_in_csv.csv`
- Parsed ESG sentence records
""",
    outputs="""
- Bar charts
- Distribution tables
""",
    when_to_use="""
Use this first to understand dataset balance and annotation coverage.
"""
)

page_doc(
    title="Tone Distribution Explorer",
    file="Tone_Distribution.py",
    purpose="""
Compute **minimum-tone distributions** per (aspect × sentiment) group.
Designed for **balancing datasets** and detecting annotation bias.
""",
    inputs="""
- `output_in_csv.csv`
- Ontologies for aspect, sentiment, tone
""",
    outputs="""
- Minimum-tone tables
- Heatmaps
- Sankey flows
""",
    when_to_use="""
Use when preparing training / evaluation datasets or auditing tone bias.
"""
)

page_doc(
    title="Sankey: Aspect → Sentiment → Tone",
    file="Sankey.py / Data_New_Distribution.py",
    purpose="""
Visualize **information flow** from aspect → sentiment → tone using Sankey diagrams.
Ontology-aware and frequency-sorted.
""",
    inputs="""
- `output_in_csv.csv`
- Ontology-normalized fields
""",
    outputs="""
- Interactive Sankey diagrams
""",
    when_to_use="""
Use when explaining ESG narrative structure or reporting patterns.
"""
)

# -------------------------------------------------------
# Model & Grounding Analysis
# -------------------------------------------------------
st.subheader("🤖 Model & Grounding Analysis")

page_doc(
    title="Model Comparison",
    file="Model Comparison tab",
    purpose="""
Compare **sentence-level outputs across LLMs** on the same document and page.
Highlights agreement, disagreement, and missing coverage.
""",
    inputs="""
- Multiple model outputs per document
- Grounded ESG sentences
""",
    outputs="""
- Comparison tables
- Highlighted markdown
""",
    when_to_use="""
Use when evaluating model reliability or selecting a preferred model.
"""
)

page_doc(
    title="Grounding Audit",
    file="Grounding Audit tab",
    purpose="""
Verify that every ESG sentence is **actually present** in the source text.
Detects hallucinations or extraction errors.
""",
    inputs="""
- Parsed ESG sentences
- Original and cleaned markdown
""",
    outputs="""
- Grounding tables
- Missing sentence alerts
""",
    when_to_use="""
Use for assurance, compliance, or regulatory review.
"""
)

# -------------------------------------------------------
# Aspect & Topic Analysis
# -------------------------------------------------------
st.subheader("🧩 Aspect & Topic Analysis")

page_doc(
    title="Aspects (Raw)",
    file="01_Aspects_Raw.py",
    purpose="""
Inspect raw extracted ESG aspects before clustering or normalization.
""",
    inputs="""
- Parsed ESG sentences
""",
    outputs="""
- Aspect frequency tables
""",
    when_to_use="""
Use when refining aspect extraction or ontology mappings.
"""
)

page_doc(
    title="Aspect Clustering",
    file="02_Aspects_Clustered.py",
    purpose="""
Group fine-grained aspects into **manual, auditable clusters**.
""",
    inputs="""
- Raw aspects
- Manual cluster JSON
""",
    outputs="""
- Clustered aspect distributions
""",
    when_to_use="""
Use when moving from sentence-level detail to thematic analysis.
"""
)

page_doc(
    title="Top Aspect Clusters",
    file="Top Aspect Clusters tabs",
    purpose="""
Highlight the **dominant ESG themes** after clustering.
""",
    inputs="""
- Clustered aspect labels
""",
    outputs="""
- Ranked cluster charts
""",
    when_to_use="""
Use for executive summaries or research insights.
"""
)

# -------------------------------------------------------
# Footer
# -------------------------------------------------------
st.markdown("---")
st.markdown("""
### ✅ Design principles

- **Ontology-aware**: Every category is explainable
- **Auditable**: Every sentence is traceable
- **Model-agnostic**: Supports multiple LLMs
- **Research-grade**: Suitable for ESG, NLP, and compliance work
""")

st.caption("ESG Dashboard · Sentence-Level · Ontology-Driven · Auditable")

