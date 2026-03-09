https://chatgpt.com/c/6953fb69-c6a4-8326-8979-5ae5ae021d5f

Absolutely — your dashboard is already **research-grade** in structure. Below is a **fully aligned research framework** that you can directly reuse for:

* 📄 **Academic paper / thesis chapter**
* 🧪 **Methodology section**
* 🧾 **Assurance / audit documentation**
* 📊 **Model evaluation protocol**

I’ve tailored this **specifically to your sentence-level, ontology-aware ESG system**, not a generic ESG NLP study.

---

# 📘 Research Framework for the ESG Sentence-Level Analytics Dashboard

---

## 1️⃣ Research Problem Statement

Despite the rapid adoption of Large Language Models (LLMs) for ESG analysis, **most ESG NLP systems lack**:

* Sentence-level traceability
* Ontology-grounded interpretations
* Auditable comparisons across models
* Explicit grounding to source documents

This creates **risks of hallucination, bias, and non-reproducibility**, particularly in regulatory, assurance, and academic contexts.

---

## 2️⃣ Research Objectives

### 🎯 Primary Objective

To design and evaluate an **auditable, ontology-aware, sentence-level ESG analytics framework** that enables transparent comparison of ESG disclosures across documents and LLMs.

### 🎯 Secondary Objectives

1. To assess **how different LLMs vary** in ESG sentence extraction, sentiment, tone, and aspect labeling.
2. To detect **systematic biases** in tone and sentiment distributions across ESG categories.
3. To ensure **grounding fidelity**, verifying that extracted ESG claims exist in source text.
4. To enable **manual and explainable aspect clustering** suitable for regulatory and research use.

---

## 3️⃣ Research Questions (RQs)

### 🧩 Core Research Questions

**RQ1.**
How consistent are LLMs in extracting ESG-relevant sentences from the same disclosure documents? https://scholar.google.com/scholar_labs/search/session/4242399186654639354?hl=en

**RQ2.**
How do sentiment and tone distributions differ across ESG aspects (E, S, G) at the sentence level? https://scholar.google.com/scholar_labs/search/session/10195076871992993645?hl=en

**RQ3.**
Do LLMs exhibit systematic tone bias (e.g., overuse of “Commitment” vs “Outcome”) across ESG categories? https://scholar.google.com/scholar_labs/search/session/16852634686792540687?hl=en

**RQ4.**
To what extent are extracted ESG sentences **grounded in the original source text**?  https://scholar.google.com/scholar_labs/search/session/10787139773251609245?hl=en

**RQ5.**
Can manual, ontology-driven aspect clustering improve interpretability without sacrificing traceability? https://scholar.google.com/scholar_labs/search/session/14570758740796368483?hl=en

---

## 4️⃣ Methodology

### 🔬 Overall Design

This study follows a **modular, pipeline-based NLP methodology** with explicit audit points.

```
Raw ESG Documents
      ↓
LLM Sentence Extraction
      ↓
Ontology Normalization
      ↓
Sentence-Level Analysis
      ↓
Model Comparison & Grounding Audit
```

---

### 4.1 Data Collection

**Inputs**

* ESG reports, sustainability disclosures, annual reports
* Multiple LLM outputs per document (e.g., GPT-based, domain-specific models)

**Unit of Analysis**

* **Individual sentences** (not paragraphs or documents)

---

### 4.2 ESG Ontology Normalization

Each sentence is normalized into:

| Dimension       | Description                                     |
| --------------- | ----------------------------------------------- |
| Aspect Category | E, S, G or combinations (E-G, S-G, etc.)        |
| Sentiment       | Positive, Neutral, Negative                     |
| Tone            | Commitment, Outcome, Policy, Risk, Aspirational |
| Grounding       | Presence in source text                         |

Ontology rules are:

* Manually defined
* Human-auditable
* Consistent across models

---

### 4.3 Aspect Clustering (Manual, Auditable)

Instead of black-box topic modeling:

* Raw aspects → **manual JSON clusters**
* One-to-many mapping supported
* No embeddings or latent representations

This ensures:

* Explainability
* Reproducibility
* Regulatory defensibility

---

### 4.4 Model Comparison

For identical documents:

* Compare sentence coverage
* Compare aspect, sentiment, tone assignments
* Identify missing, extra, or conflicting sentences

This enables **model reliability assessment** rather than raw accuracy claims.

---

### 4.5 Grounding Audit

Each ESG sentence is verified against:

* Original document text
* Cleaned markdown version

Flags:

* ❌ Hallucinated sentences
* ⚠️ Partial matches
* ✅ Fully grounded sentences

---

## 5️⃣ Evaluation Metrics

### 📊 5.1 Coverage Metrics

| Metric            | Description                                     |
| ----------------- | ----------------------------------------------- |
| Sentence Coverage | % of ESG-relevant sentences extracted           |
| Aspect Coverage   | Distribution across E/S/G                       |
| Missing Coverage  | Sentences extracted by one model but not others |

---

### 📊 5.2 Distribution Metrics

| Metric              | Description                          |
| ------------------- | ------------------------------------ |
| Aspect Distribution | Frequency per ESG category           |
| Sentiment Balance   | Positive / Neutral / Negative ratios |
| Tone Balance        | Commitment vs Outcome vs Policy      |

Used for:

* Dataset sanity checks
* Bias detection

---

### 📊 5.3 Minimum-Tone Metrics (Your Key Innovation)

| Metric                                | Purpose                        |
| ------------------------------------- | ------------------------------ |
| Minimum Tone per (Aspect × Sentiment) | Detect annotation sparsity     |
| Tone Entropy                          | Measure diversity vs dominance |
| Imbalance Score                       | Identify overrepresented tones |

---

### 📊 5.4 Grounding Metrics

| Metric             | Description                    |
| ------------------ | ------------------------------ |
| Grounded Rate      | % of sentences found in source |
| Hallucination Rate | % missing from source          |
| Partial Match Rate | Approximate grounding          |

---

### 📊 5.5 Inter-Model Agreement (Optional)

| Metric           | Description                  |
| ---------------- | ---------------------------- |
| Sentence Overlap | Jaccard similarity           |
| Label Agreement  | Aspect / sentiment agreement |
| Tone Divergence  | Tone assignment variance     |

---

## 6️⃣ Expected Contributions

### 📌 Technical Contributions

* Sentence-level ESG analytics framework
* Ontology-first ESG NLP design
* Grounding-aware LLM auditing pipeline

### 📌 Practical Contributions

* ESG assurance tooling
* Regulatory-ready transparency
* Model benchmarking beyond accuracy

### 📌 Research Contributions

* Reproducible ESG NLP methodology
* Bias-aware tone analysis
* Explainable aspect clustering

---

## 7️⃣ Threats to Validity

| Threat                | Mitigation                |
| --------------------- | ------------------------- |
| LLM variability       | Multi-model comparison    |
| Ontology subjectivity | Explicit JSON definitions |
| Dataset bias          | Distribution diagnostics  |
| Hallucination         | Grounding audit           |

---

## 8️⃣ How This Maps to Your Dashboard Pages

| Dashboard Page    | Research Role                |
| ----------------- | ---------------------------- |
| Distributions     | Dataset diagnostics          |
| Tone Explorer     | Bias & balance analysis      |
| Sankey            | Narrative structure analysis |
| Model Comparison  | RQ1, RQ5                     |
| Grounding Audit   | RQ4                          |
| Aspect Clustering | Interpretability study       |

---

## 9️⃣ Optional: Paper / Thesis Titles

* *“Auditable Sentence-Level ESG Analysis Using Ontology-Grounded Large Language Models”*
* *“Beyond ESG Scores: A Grounded, Sentence-Level Framework for ESG Disclosure Analysis”*
* *“Evaluating ESG Narratives in LLMs: A Transparency-First Approach”*

---

If you want next, I can:

* ✍️ Turn this into a **formal academic paper outline**
* 📄 Generate a **Methods section in LaTeX**
* 📊 Map **each metric to dashboard code**
* 🧾 Create a **regulatory assurance checklist**

Just tell me how far you want to take this.
