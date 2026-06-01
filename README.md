# esg-birru

Streamlit prototype for an ESG certification/rating workflow with:
- Role-based login (Admin / Company / Auditor / Company_Aggregator)
- Level 1 self-assessment (JSON-backed)
- Level 2 evidence upload + auditor decision (JSON-backed)
- Simple graph explorer (JSON → NetworkX render)
- Simple industry “clustering” (centroid over Level 1 scores)

This repo is intentionally file-based (JSON under `backend/db/json_db/`) to keep the prototype easy to run and iterate.

## Quickstart

### 1) Create a virtualenv + install deps

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### 2) Run the app

```bash
. .venv/bin/activate
streamlit run streamlit_app/app.py
```

## Seed accounts

Seed users are stored in `backend/db/json_db/users.json`.

Example credentials (dev-mode): the `password_hash` field is treated as plain text in this prototype.

- `admin@certify.com` / `HASH_ADMIN` (roles: Admin)
- `alice@acme.com` / `HASH_1` (roles: Company)
- `audit@acme.com` / `HASH_2` (roles: Company, Auditor)
- `group-lead@megagroup.com` / `HASH_3` (roles: Company_Aggregator)

## Data storage

- DB root: `backend/db/json_db/`
- Common files:
  - `users.json`
  - `companies.json`
  - `assessments_level1.json`
  - `assessments_level2.json`
  - `documents.json`
  - `ocr_results.json`
  - `graph_store.json`
  - `clusters.json`

Uploads (Level 2 evidence) are written under `storage/uploads/<company_id>/`.

## Notable implementation details

- Routing/navigation: `streamlit_app/app.py`
- Auth/RBAC: `streamlit_app/utils/auth_utils.py`
- JSON IO helpers: `streamlit_app/utils/data_access.py`
- Path handling: `streamlit_app/utils/paths.py`

## Known limitations (prototype)

- Authentication is dev-mode (plain text compare) and is not secure for production.
- There is no automated test suite in this repo yet.
- Several pages are minimal “scaffolding” that currently just display JSON.

## Notes

The previous long-form design notes and schemas were moved to `notes.md`.

---

## Project Overview

`esg-birru` is a Streamlit-based prototype that demonstrates a lightweight ESG certification workflow for SMEs and certifiers:

- Companies can complete a Level 1 self-assessment and optionally upload supporting evidence.
- Auditors/admins can review evidence and record Level 2 verification decisions.
- The system stores data in JSON files (instead of a database) to keep iteration fast and transparent.

The main problem it solves (in prototype form): providing a structured, evidence-aware ESG assessment flow that can be extended later into a production architecture (e.g., Postgres/Neo4j, real auth, services).

## Tech Stack

- Language: Python 3
- UI framework: Streamlit
- Libraries:
  - `networkx` + `matplotlib` (graph preview)
  - `pillow` + `pytesseract` (OCR-related dependencies; OCR page is scaffolded)
  - `bcrypt` (installed, but this prototype currently uses dev-mode plain-text password comparison)

Dependencies are listed in `requirements.txt`.

## Architecture Overview

High-level components:

- `streamlit_app/app.py`: Router + navigation. Dynamically imports page modules and calls their `run(st)` function.
- `streamlit_app/pages/*`: Individual pages (Login, Dashboard, L1/L2, Graph Explorer, etc.).
- `streamlit_app/utils/*`:
  - `auth_utils.py`: Session + login + RBAC gatekeeping for pages.
  - `paths.py`: Single source of truth for repo-relative paths.
  - `data_access.py`: JSON load/write helpers.
- `backend/db/json_db/*`: File-based “database” (seed users, companies, assessments, etc.).
- `storage/uploads/*`: Uploaded evidence files (Level 2).

Data flow (typical):

1. User logs in (`users.json`) → session state stores `user_id`.
2. Level 1 / Level 2 pages read and write JSON files under `backend/db/json_db/`.
3. Evidence uploads are saved to disk and referenced from `documents.json`.

## Installation & Setup

### Prerequisites

- Python 3.10+ (tested with Python 3.12)

Optional (for OCR features):
- Tesseract installed on your system (`pytesseract` is only a wrapper).

### Setup steps

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

### Run locally

```bash
. .venv/bin/activate
streamlit run streamlit_app/app.py
```

## Usage Guide

### Log in

1. Open the app in your browser (Streamlit prints the local URL).
2. Go to **Login**.
3. Use one of the seed accounts from `backend/db/json_db/users.json`.

Example:
- Email: `admin@certify.com`
- Password: `HASH_ADMIN`

### Company flow (Level 1 → Level 2 evidence)

1. Log in as a Company user (e.g. `alice@acme.com` / `HASH_1`).
2. Go to **Assessment (Level 1)** to view existing Level 1 JSON data (this page is currently minimal).
3. Go to **Assessment (Level 2)** or **Upload Document** to upload evidence.
4. Verify a new entry is appended to `backend/db/json_db/documents.json`.

### Auditor flow (review evidence)

1. Log in as an Auditor-capable user (e.g. `audit@acme.com` / `HASH_2`) or Admin.
2. Go to **Assessment (Level 2)**.
3. Select a pending document and apply a decision.
4. Verify a new entry is appended to `backend/db/json_db/assessments_level2.json`.

### Graph Explorer

1. Log in.
2. Go to **Graph Explorer**.
3. Add nodes/edges (saved to `backend/db/json_db/graph_store.json`).
4. Click **Render preview** to see a quick NetworkX visualization.

## API Reference (if applicable)

This repo does not expose a separate HTTP API at the moment.

If you later add an API layer, the natural boundary is `backend/` (currently used only for JSON data files).

## Environment Variables

No `.env` is required for the current prototype.

If you plan to productionize, typical variables you may introduce:

- `APP_ENV` (e.g., `dev`, `prod`)
- `DB_URL` (Postgres connection string)
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`
- `STREAMLIT_SERVER_PORT`
- `AUTH_MODE` (e.g., `dev_plaintext`, `bcrypt`)

## Contributing Guide

- Keep changes small and focused.
- Prefer updating `streamlit_app/utils/paths.py` (or using its helpers) rather than introducing new ad-hoc path logic.
- JSON data lives under `backend/db/json_db/`; avoid committing large uploaded files under `storage/` unless explicitly needed.

Suggested workflow:

1. Create a new branch.
2. Make changes with clear, scoped commits.
3. Run `python -m compileall -q .` in your venv.
4. Open a PR describing what changed and how to test it.

## License

No license file is included yet.

If you want this to be open source, add a `LICENSE` file (MIT, Apache-2.0, or GPL-3.0 are common choices) and update this section accordingly.

---

## Scaling Guide

This repo is a JSON-backed Streamlit prototype. Under load, the first things to fail will be shared-file writes, single-process bottlenecks, and lack of isolation between users/sessions. The notes below describe a realistic path from MVP → production-grade.

### 1) Current Bottlenecks (what breaks first)

- **JSON files as a “DB”**: concurrent writes to `backend/db/json_db/*.json` will eventually cause lost updates (last writer wins), partial writes, or corruption.
- **No locking/transactions**: uploads + JSON update aren’t atomic across processes.
- **Single Streamlit process**: Streamlit apps typically run as a single Python process per replica; CPU-heavy tasks (OCR, graph ops) will block requests.
- **Local filesystem uploads**: `storage/uploads/...` does not scale across multiple instances without shared storage.
- **Session/auth model**: `st.session_state` is per-process/per-browser session; multiple replicas require sticky sessions or moving auth/session to a shared store.
- **Observability gaps**: no structured logging/metrics/tracing; diagnosing performance and errors under load becomes guesswork.

### 2) Database Scaling

#### Step 0: Replace JSON with a real DB

Recommended baseline:
- **PostgreSQL** for users/companies/assessments/documents/audit logs.
- Optional: **Neo4j** (or Postgres + `pgvector` / graph tables) if you truly need graph queries beyond simple visualization.

#### Indexing (Postgres)

Likely indexes (based on current JSON fields):
- `users(email)` unique index
- `documents(company_id)`, `documents(assessment_id)`, `documents(ocr_status)`
- `assessments_level1(company_id, submitted_at)`
- `assessments_level2(company_id, completed_at)`

#### Caching

- Add **Redis** for:
  - session tokens / rate limits
  - caching “dashboard stats” aggregates
  - caching expensive report computations

#### Read scaling

- Start with **read replicas** once read traffic dominates writes (dashboards, reports, analytics).
- Move heavy analytics to a warehouse later (BigQuery/Snowflake/Redshift) if needed.

#### Sharding

Avoid sharding early. When you truly need it, a natural shard key is:
- `company_id` (most queries are tenant/company scoped)

### 3) Backend Scaling

Streamlit is great for prototypes, but for production scale you’ll typically split into:

- **Frontend/UI**: Streamlit (kept) or migrate to a web app (React/Next.js).
- **Backend API**: FastAPI (or Django) serving JSON APIs.
- **Workers**: background jobs for OCR/media processing/report generation.

Recommended scaling patterns:

- **Horizontal scaling**: run multiple API replicas behind a load balancer (preferred).
- **Vertical scaling**: only as a quick stopgap for CPU/RAM bound workloads.
- **Async + job queue**: OCR and other long-running tasks should run in workers, not in the request path.

Operationally:
- Put a **load balancer** in front of the API.
- Use **autoscaling** based on CPU/RPS/queue depth.
- Ensure all instances are stateless; store sessions in Redis and files in object storage.

### 4) Frontend Scaling

Current UI is Streamlit (server-rendered Python). Options:

- **Keep Streamlit**:
  - Put Streamlit behind a reverse proxy.
  - Scale with multiple replicas + sticky sessions (or move auth state out of `st.session_state`).
  - Offload heavy compute to worker services.

- **Move to a JS frontend** (for large scale / better UX):
  - Use **CDN** for static assets.
  - Implement **lazy loading** for heavy pages (reports/graphs).
  - Consider **SSR/SSG** with Next.js for marketing/docs pages; keep the authenticated app as SPA/SSR as needed.

Even with Streamlit, you can still use a CDN for:
- static exports (reports, images)
- public documentation site

### 5) Infrastructure (recommended cloud setup)

Two realistic setups:

#### Option A (fastest MVP-to-prod): Managed containers + managed DB

AWS example (similar services exist on GCP/Azure):
- Compute:
  - **ECS Fargate** (or EKS later) for API + workers + Streamlit
  - **Application Load Balancer** in front
- Data:
  - **RDS Postgres** for relational data
  - **ElastiCache Redis** for cache/sessions/queues
  - **S3** for uploads and generated reports
- Async processing:
  - **SQS** (queue) + worker tasks
- Observability:
  - **CloudWatch** logs/metrics, or OpenTelemetry → Datadog/Grafana

#### Option B (serverless leaning): API + queues + object storage

- API: **AWS Lambda** (works best if requests are short and dependencies are manageable)
- Queue/workers: **SQS + Fargate workers** (keep OCR off Lambda if it’s heavy)
- DB: **RDS Postgres**
- Files: **S3**

### 6) Cost Estimate (very rough)

These are order-of-magnitude ranges for a typical SaaS-style workload. Real cost depends on:
requests per user, file upload sizes, OCR/media processing volume, retention, and concurrency.

- **~1k users** (low concurrency, light OCR):
  - ~$50–$250/month
  - Single small DB, 1–2 small containers, minimal Redis, small object storage.

- **~10k users** (moderate concurrency, some background jobs):
  - ~$300–$2,000/month
  - Multi-replica API/Streamlit, Redis, larger Postgres, queue + workers, more storage/egress.

- **~100k users** (high concurrency, frequent jobs/analytics):
  - ~$3,000–$30,000+/month
  - Autoscaling fleets, read replicas, heavier caching, dedicated workers, stronger observability, possibly a data warehouse.

If you share expected “active users/day”, average session length, and OCR volume, you can tighten this to a more meaningful estimate.

### 7) Roadmap (MVP → production-grade)

1. **Stabilize data model**
   - Define canonical schemas for users/companies/assessments/documents/audit logs.
2. **Move off JSON**
   - Migrate to Postgres; add migrations (Alembic/Django migrations).
3. **Externalize storage**
   - Move uploads from local disk to S3 (or GCS/Azure Blob) and store only URLs/metadata in DB.
4. **Split compute from UI**
   - Introduce FastAPI for data operations; keep Streamlit as a thin client calling the API.
5. **Add background processing**
   - Queue + workers for OCR/media/report generation; add retries and idempotency keys.
6. **Add auth & tenancy**
   - Replace dev-mode auth with proper password hashing + sessions/JWT + RBAC checks at the API layer.
7. **Observability + reliability**
   - Centralized logs, metrics, tracing; alerts on error rates/latency/queue depth.
8. **Scale reads**
   - Caching for dashboards/reports; add read replicas if needed.
9. **Hardening**
   - Rate limiting, input validation, security reviews, backups, DR plan.
10. **Performance tuning**
   - Indexing, query optimization, batch processing, pagination, and load testing.

---

## Similar Products / Market Landscape

Below are 10 products/companies in the broader “ESG assessment / sustainability reporting / supplier due diligence / evidence + scoring” space. Details like tech stack and scale are based on public information; many vendors don’t disclose their implementation details, so “tech stack” is marked as “not public” where appropriate.

### 1) EcoVadis

- What they do: Sustainability ratings/scorecards for companies (often used in supply chains for vendor screening and improvement programs).
- Tech stack (public): Not publicly disclosed (SaaS platform).
- Business model: Subscription / per-rating / enterprise programs (B2B).
- Scale (public): Reports having **130,000+ rated companies** in its database (as of end of 2023). Source: `https://support.ecovadis.com/hc/en-us/articles/210459707-Who-are-EcoVadis-customers`
- What makes them successful:
  - Strong network effects (buyers request EcoVadis ratings from suppliers).
  - Standardized methodology and benchmarking across industries.
  - Clear “scorecard” output that procurement teams can operationalize.

### 2) Sedex (and SMETA ecosystem)

- What they do: Supplier ethical/sustainability data exchange + assessment/audit workflow (SMETA audits) for supply chain due diligence.
- Tech stack (public): Not publicly disclosed (SaaS platform).
- Business model: Membership/subscription (B2B).
- Scale (public): Not consistently published in one canonical place; public materials describe broad global adoption. Start here: `https://www.sedex.com/`
- What makes them successful:
  - Deep procurement + audit ecosystem adoption (buyers, suppliers, auditors).
  - A common audit/reporting language (SMETA) that reduces duplication.

### 3) Workiva (Sustainability / ESG reporting)

- What they do: Connected reporting and disclosure platform spanning financial reporting, GRC, and sustainability reporting workflows.
- Tech stack (public): Not fully disclosed; cloud SaaS platform.
- Business model: Subscription SaaS (mid-market to enterprise).
- Scale (public): Reports **6,624 customers** (as of December 31, 2025). Source: `https://investor.workiva.com/node/12036/html`
- What makes them successful:
  - Excellent “data → disclosure” workflow and controls.
  - Enterprise-grade governance/auditability and integrations.
  - Strong retention and expansion in large accounts.

### 4) Salesforce Net Zero Cloud

- What they do: Carbon/ESG data management and reporting, designed to sit alongside CRM/supply-chain data.
- Tech stack (public): **Built on the Salesforce platform**.
- Business model: Subscription (Salesforce product editions/add-ons).
- Scale (public): Not publicly disclosed as a user count; benefits from Salesforce’s enterprise install base.
- What makes them successful:
  - Distribution: ships into organizations already standardized on Salesforce.
  - Integrates sustainability data with operational/business data.

### 5) IBM Envizi

- What they do: Emissions accounting and sustainability performance management (Scope 1/2/3, auditability, reporting).
- Tech stack (public): Not fully disclosed; enterprise SaaS (IBM product).
- Business model: Subscription / enterprise contracts.
- Scale (public): Not publicly disclosed; positioned as enterprise-grade and used by large organizations.
- What makes them successful:
  - Enterprise credibility + integration story (IBM ecosystem).
  - Focus on audit trail and reporting readiness.

### 6) Persefoni

- What they do: “Carbon accounting and climate management” platform emphasizing calculation methodology, audit trail, and reporting.
- Tech stack (public): Not fully disclosed; SaaS platform; public partnerships indicate embedded analytics components.
- Business model: Subscription SaaS (enterprise + mid-market tiers).
- Scale (public): Not consistently disclosed; positioned as enterprise-grade and methodologically rigorous.
- What makes them successful:
  - Methodology credibility and auditability focus.
  - Strong product narrative around assurance-grade disclosures.

### 7) Watershed

- What they do: Enterprise sustainability platform (carbon accounting + decarbonization planning + reporting).
- Tech stack (public): Not publicly disclosed (SaaS platform).
- Business model: Subscription + services (enterprise).
- Scale (public): Not publicly disclosed; widely positioned as an enterprise platform.
- What makes them successful:
  - Strong “platform + expertise” story (tools plus climate advisory partners).
  - Focus on executive-ready reporting and planning.

### 8) Sphera (EHS / sustainability / risk)

- What they do: Enterprise EHS and sustainability management platform (operational risk + sustainability data management).
- Tech stack (public): Not publicly disclosed (SaaS platform).
- Business model: Enterprise subscription + services.
- Scale (public): Markets **8,400+ customers** across industries (some materials also cite 8,500+). Source: `https://sphera.com/press-releases-from-sphera/`
- What makes them successful:
  - Broad coverage across EHS + sustainability, embedded in operations.
  - Large legacy customer base and long-term procurement relationships.

### 9) RepRisk

- What they do: ESG risk intelligence and due diligence data (media-based signals, controversies, risk screening).
- Tech stack (public): Not publicly disclosed; data/analytics product delivered via platforms and integrations.
- Business model: Subscription (financial services + enterprise risk/procurement).
- Scale (public): Public statements cite **350+ clients globally** (historical milestone; current may be higher). Source: `https://www.businesswire.com/news/home/20200720005510/en/RepRisk-Reaches-New-Milestone-of-Evaluating-More-Than-150000-Companies-on-ESG-Risks`
- What makes them successful:
  - High-signal risk monitoring that complements self-reported data.
  - Integrates into financial/procurement workflows as a “screening layer”.

### 10) MSCI ESG Ratings / Sustainalytics ESG Risk Ratings (investor-grade ratings providers)

- What they do: Investor-facing ESG ratings/research and datasets used for portfolio analysis, screening, and benchmarking.
- Tech stack (public): Not publicly disclosed (data + research products).
- Business model: Data subscription / enterprise licensing.
- Scale (public): Large company coverage universes (examples: MSCI’s ESG Ratings brochure cites 8,500 company ratings; Sustainalytics markets 16,000+ companies covered for ESG Risk Ratings). Sources: `https://www.msci.com/documents/1296102/15233886/MSCI-ESG-Ratings-Brochure-cbr-en.pdf` and `https://www.sustainalytics.com/corporate-solutions/esg-risk-ratings`
- What makes them successful:
  - Embedded into investment and index construction workflows.
  - Longstanding brand trust, methodology governance, and dataset breadth.

### What could differentiate `esg-birru` (niche opportunities)

Most “successful” platforms win via network effects (procurement ecosystems), auditability, and tight integration into existing enterprise systems. For this project, realistic differentiation paths include:

- **SME-first evidence workflow**: Make evidence upload, OCR extraction, and “what counts as evidence” extremely simple for SMEs (who often lack ESG staff).
- **Assurance-grade audit trail**: Treat every score as a traceable claim with linked evidence, reviewer actions, and reproducible calculations.
- **Human-in-the-loop scoring**: Provide tools that let auditors/certifiers efficiently review, override, and explain model outputs with clear provenance.
- **Vertical specialization**: Pick one industry segment (e.g., manufacturing SMEs) and ship templates/questions/evidence rules that are “opinionated and correct” for that niche.
- **Buyer/supplier collaboration**: Even without becoming “the network”, support invitation flows where a buyer requests a supplier assessment and tracks completion.
- **Compliance alignment as product UX**: Help users map outputs to CSRD/ISSB/GRI-style disclosure requirements with minimal manual work.
