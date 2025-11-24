Below is a **full, scalable, production-ready directory structure** for your Streamlit-based certification platform **with multi-role users, Level 1 & Level 2 assessments, OCR/media verification, graph-based reasoning, and clustering by industry**.
I also include **complete JSON-based data structures** that can later be migrated to **PostgreSQL + Neo4j**.

---

https://chatgpt.com/c/69246b65-4da8-832d-abeb-62001e2bd43b

# ✅ **1. Project Directory Structure (Full Production-Ready Design)**

```
certify_app/
│
├── streamlit_app/
│   ├── app.py                                 # Main entry point (routing)
│   ├── pages/
│   │   ├── 01_Login.py
│   │   ├── 02_Dashboard.py
│   │   ├── 03_Company_Assessment_Level1.py
│   │   ├── 04_Company_Assessment_Level2.py
│   │   ├── 05_Document_Uploader.py
│   │   ├── 06_OCR_Processor.py
│   │   ├── 07_Media_Checker.py
│   │   ├── 08_Graph_Explorer.py
│   │   ├── 09_Reports_Level1.py
│   │   ├── 10_Reports_Level2.py
│   │   ├── 11_Aggregator_Company_Overview.py
│   │   ├── 12_Admin_Question_Editor.py
│   │   ├── 13_Admin_User_Manager.py
│   │   ├── 14_Industry_Clustering.py
│   │   └── 15_API_Diagnostics.py
│   │
│   ├── components/                             # Reusable Streamlit UI blocks
│   │   ├── auth.py
│   │   ├── cards.py
│   │   ├── layout.py
│   │   ├── charts.py
│   │   └── tables.py
│   │
│   ├── utils/
│   │   ├── auth_utils.py
│   │   ├── file_utils.py
│   │   ├── ocr_utils.py
│   │   ├── media_utils.py
│   │   ├── graph_utils.py
│   │   ├── clustering.py
│   │   └── report_generator.py
│   │
│   └── config/
│       ├── app_config.yaml
│       ├── roles_permissions.json
│       └── industry_map.json
│
├── backend/                                   # Future microservice layer
│   ├── api/
│   │   ├── auth_api.py
│   │   ├── ocr_api.py
│   │   ├── media_api.py
│   │   ├── graph_api.py
│   │   └── report_api.py
│   ├── db/
│   │   ├── json_db/                            # Initial DB (file-based)
│   │   │   ├── users.json
│   │   │   ├── companies.json
│   │   │   ├── assessments.json
│   │   │   ├── documents.json
│   │   │   ├── media_checks.json
│   │   │   ├── graph_store.json
│   │   │   └── clusters.json
│   │   ├── neo4j/                              # For future migration
│   │   │   ├── init_graph.cypher
│   │   │   └── schema.cypher
│   │   └── migrations/
│   ├── services/
│   │   ├── user_service.py
│   │   ├── assessment_service.py
│   │   ├── document_service.py
│   │   ├── ocr_service.py
│   │   ├── media_service.py
│   │   ├── graph_service.py
│   │   └── clustering_service.py
│   └── models/
│       ├── user_model.py
│       ├── company_model.py
│       ├── assessment_model.py
│       ├── ocr_result_model.py
│       ├── media_result_model.py
│       └── graph_model.py
│
├── ai_modules/
│   ├── ocr/                                   # PaddleOCR / Tesseract
│   ├── media/
│   │   ├── social_scraper/
│   │   ├── news_scraper/
│   │   ├── sentiment/
│   │   └── stance/
│   ├── graph_reasoning/
│   ├── llm_explainability/
│   └── clustering/
│
├── storage/
│   ├── uploads/
│   │   ├── raw_documents/
│   │   ├── processed_documents/
│   │   └── media_screenshots/
│   ├── cache/
│   └── logs/
│       ├── access.log
│       ├── ocr.log
│       └── media_checker.log
│
├── tests/
│   ├── test_api.py
│   ├── test_graph.py
│   ├── test_ocr.py
│   ├── test_media.py
│   ├── test_clustering.py
│   └── test_streamlit_pages.py
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# ✅ **2. Multi-Role Access Structure**

### Roles

```
Admin
Company
Company_Aggregator
Auditor / Certifier
```

### Permissions (example)

```
Admin:
  - manage_users
  - edit_questions
  - view_all_reports

Company:
  - submit_assessment
  - upload_documents
  - view_own_reports

Company_Aggregator:
  - view_company_status
  - download_company_reports

Auditor:
  - verify_documents
  - run_level2_checks
  - generate_final_report
```

---

# ✅ **3. Data Structure (JSON → scalable DB)**

Below are **fully defined schemas** for the system.

---

## **3.1 User JSON Structure**

```json
{
  "id": "user_124",
  "role": ["Company", "Company_Aggregator"],
  "email": "contact@acme.com",
  "password_hash": "HASHED_PASSWORD",
  "company_id": "comp_001",
  "created_at": "2025-11-24T10:00:00Z"
}
```

---

## **3.2 Company Structure**

```json
{
  "id": "comp_001",
  "name": "ACME Manufacturing",
  "industry": "Manufacturing",
  "address": "123 Road, Finland",
  "created_at": "2025-11-24T10:00:00Z",
  "certification_status": {
    "level1": "completed",
    "level2": "in_progress"
  }
}
```

---

## **3.3 Assessment Structure**

Each company has many assessments.

```json
{
  "assessment_id": "assess_1003",
  "company_id": "comp_001",
  "level": 1,
  "question_id": "Q-14",
  "question_type": "multiple_choice",
  "answer": ["Option A", "Option D"],
  "score": 0.82,
  "submitted_at": "2025-11-24T09:12:00Z",
  "reviewer": null,
  "linked_documents": ["doc_201", "doc_202"],
  "explainability": {
    "llm_reasoning": "The selected options indicate strong compliance.",
    "graph_relations": ["node_21 -> node_88"]
  }
}
```

---

## **3.4 Document Upload Structure**

```json
{
  "doc_id": "doc_201",
  "company_id": "comp_001",
  "assessment_id": "assess_1003",
  "filename": "ISO9001_certificate.pdf",
  "file_path": "/uploads/raw_documents/comp_001/",
  "ocr_status": "processed",
  "ocr_result_id": "ocr_224",
  "uploaded_at": "2025-11-24T10:20:00Z"
}
```

---

## **3.5 OCR Results**

```json
{
  "ocr_id": "ocr_224",
  "doc_id": "doc_201",
  "extracted_text": "This certifies that ACME ...",
  "named_entities": [
    { "type": "ORG", "value": "ACME" },
    { "type": "DATE", "value": "2023-08-22" }
  ],
  "confidence_score": 0.91,
  "processed_at": "2025-11-24T10:22:10Z"
}
```

---

## **3.6 Media Checker Structure**

```json
{
  "media_id": "media_509",
  "company_id": "comp_001",
  "platform": "news",
  "source_url": "https://example.com/article",
  "content_text": "ACME faces investigation for ...",
  "sentiment": -0.6,
  "stance": "negative",
  "relevance_score": 0.72,
  "verified_date": "2025-11-24T11:05:00Z"
}
```

Supports **Twitter/X, Facebook, LinkedIn, Reddit, Local News APIs**.

---

## **3.7 Graph Database JSON (pre-Neo4j)**

```json
{
  "nodes": [
    { "id": "node_21", "type": "Company", "name": "ACME" },
    { "id": "node_88", "type": "Document", "name": "ISO9001" }
  ],
  "edges": [
    {
      "source": "node_21",
      "target": "node_88",
      "relation": "HAS_DOCUMENT"
    }
  ]
}
```

---

## **3.8 Cluster Structure (by Industry)**

```json
{
  "industry": "Manufacturing",
  "clusters": [
    {
      "cluster_id": "mfg_cluster_01",
      "description": "High compliance, strong documentation",
      "companies": ["comp_001", "comp_005"],
      "centroid_features": {
        "avg_level1_score": 0.83,
        "avg_level2_score": 0.79,
        "media_risk": 0.12
      }
    }
  ]
}
```

---

# ✅ **4. How the Certification Pipeline Works**

### **Level 1**

✔ Company answers questions
✔ Auto-score
✔ Store in JSON
✔ Generate explainability (LLM)
✔ Level 1 Report

---

### **Level 2**

✔ Company uploads evidence
✔ OCR
✔ News/Social media scraping (1–2 years)
✔ Media sentiment, stance, fact-checking
✔ Graph linking (Company → Document → Risk)
✔ Industry clustering
✔ Level 2 Explainability
✔ Final certification report

---

# ✅ **5. Want me to generate ALL .py files?**

I can generate:

✔ `app.py` (Streamlit router)
✔ Full `pages/*.py` page code
✔ Data access layer
✔ JSON read/write functions
✔ Graph ingestion scripts
✔ OCR/Media utils
✔ Auto-report generator (Level 1 + Level 2)

Just tell me:

**“Generate me the entire backend code”**
or
**“Start with app.py + Login page”**

I can deliver everything in clean, production-ready style.

👉 Next: Batch 4?

Batch 4 can include:

🔥 Migration-ready SQL schema (PostgreSQL)
🔥 Migration-ready Neo4j graph schema
🔥 API endpoint designs for each dataset
🔥 Full example queries (Cypher, SQL, Streamlit functions)# esg-birru
