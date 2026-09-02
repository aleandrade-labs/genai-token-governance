# 🏛️ Enterprise GenAI Token & Label Governance: Ingestion Architecture Guide

**Audience:** Chief Information Officers (CIO), Chief Technology Officers (CTO), FinOps Directors, Cloud Architects, AI Platform Leads  
**Official Reference:** [Google Agent Development Kit (ADK) — BigQuery Agent Analytics](https://adk.dev/integrations/bigquery-agent-analytics/)  
**Target Environment:** Google Cloud Vertex AI, BigQuery, Looker Studio  

---

## 🎯 Executive Overview

To achieve **real-time GenAI Financial Chargeback** (SAP ERP Cost Centers) and **Strategic Value Governance** (`qualificado_como`, `valor`, `budget_usd`), enterprise engineering teams must capture token-level telemetry from LLM calls and ingest it into Google BigQuery.

There are **4 primary architectural patterns** to instrument and stream this telemetry on Google Cloud. This document provides an exhaustive, side-by-side comparison of each method, complete with working code examples, trade-offs, ingestion latencies, and a decision framework.

---

## 📊 Comprehensive Comparison Matrix

| Dimension | 1. Official Google ADK Plugin | 2. Direct BigQuery Streaming SDK | 3. Cloud Logging Log Router Sink | 4. Batch Loading (`bq load` / GCS) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Reference File** | [`src/run_official_adk_agent.py`](../src/run_official_adk_agent.py) | [`src/run_live_gemini_batch.py`](../src/run_live_gemini_batch.py)<br>[`src/interactive_chat.py`](../src/interactive_chat.py) | [`src/adk_interceptor/finops_wrapper.py`](../src/adk_interceptor/finops_wrapper.py) | [`src/live_gemini_generator.py`](../src/live_gemini_generator.py) |
| **Underlying Ingestion Protocol** | **BigQuery Storage Write API** (gRPC streaming) | **BigQuery Streaming API** (`insert_rows_json`) | **Cloud Logging Router** $\rightarrow$ BigQuery Sink | **BigQuery Batch Load Job** (JSONL / Parquet) |
| **Ingestion Latency / Delay** | ⚡ **< 1 second (Sub-second)** | ⚡ **< 1 second (Sub-second)** | ⏳ **2 to 10 seconds** | ⏳ **5 to 30 seconds** (Batch job runtime) |
| **Looker Studio Availability** | **Immediate upon refresh** (`Cmd+Shift+R`) | **Immediate upon refresh** | **Available in ~5-10s** | **Available after job finishes** |
| **Agentic Tool Telemetry** | ✅ **Automated native capture** of all function calls & tools | ✅ Fully supported via manual or wrapper hooks | ⚠️ Requires manual JSON payload construction | ⚠️ Requires batch logging formatting |
| **Multi-Turn Reasoning Spans** | ✅ **Automated trace & span linking** across agent turns | ✅ Fully customizable span/trace hierarchy | ⚠️ Log-based correlation | ❌ Flat record format |
| **Schema Management** | ✅ **Auto-schema upgrade** & auto-creates analytical views | ⚠️ Managed via BigQuery DDL table definitions | ⚠️ BigQuery sink handles basic schema evolution | ⚠️ Table schema must pre-exist or use autodetect |
| **Application Footprint** | Requires `google-adk` | Requires `google-cloud-bigquery` | **Zero BigQuery SDK** (Standard Python `logging`) | Zero live SDK (Writes file, loads out-of-band) |
| **Network & Security** | gRPC (Port 443) / IAM ADC | REST HTTPS / IAM ADC | REST HTTPS / Cloud Logging IAM | REST HTTPS / GCS IAM |

---

## 🔍 Option 1: Official Google ADK Plugin (`BigQueryAgentAnalyticsPlugin`)

### 🧠 How It Works
The [Google Agent Development Kit (ADK)](https://adk.dev) provides a native, production-grade observability plugin: `BigQueryAgentAnalyticsPlugin`. When attached to an ADK `Runner`, it hooks directly into the agent's internal lifecycle, automatically streaming traces, multi-turn reasoning steps, tool calls, and custom policy tags via the high-performance **BigQuery Storage Write API**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                OPTION 1: GOOGLE ADK NATIVE                             │
│                                                                                        │
│  ┌───────────────────────┐                                                             │
│  │   Google ADK Agent    │                                                             │
│  │  (Multi-Agent Swarm)  │                                                             │
│  └──────────┬────────────┘                                                             │
│             │                                                                          │
│             ▼                                                                          │
│  ┌────────────────────────────────────────┐                                            │
│  │  BigQueryAgentAnalyticsPlugin          │                                            │
│  │  • Custom SAP ERP Policy Tags          │                                            │
│  │  • Automated Tool Call Interception    │                                            │
│  │  • Storage Write API gRPC Stream       │                                            │
│  └──────────────────┬─────────────────────┘                                            │
│                     │                                                                  │
│                     ▼  (Sub-second gRPC Stream)                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                 Google Cloud BigQuery (`genai_finops_governance`)                │  │
│  │  • Table: `adk_events`                                                           │  │
│  │  • Auto-Generated Views: `v_adk_executive_kpis`, `v_adk_user_leaderboard`        │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 💻 Production Code Implementation

```python
import asyncio
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.plugins.bigquery_agent_analytics_plugin import (
    BigQueryAgentAnalyticsPlugin,
    BigQueryLoggerConfig
)

# 1. Define your Agent with Tools
def sap_erp_billing_lookup(customer_cnpj: str) -> str:
    """Query SAP ERP for billing history and energy consumption."""
    return f"SAP Record for {customer_cnpj}: Grupo A4, Demanda 1200 kW."

agent = Agent(
    name="vendas_agent",
    instruction="Auxilie os clientes na contratação de energia no Mercado Livre.",
    tools=[sap_erp_billing_lookup]
)

# 2. Instantiate the Official BigQuery Analytics Plugin
plugin = BigQueryAgentAnalyticsPlugin(
    project_id="aleorg-dev-workload-01",
    dataset_id="genai_finops_governance",
    table_id="adk_events",
    location="us-central1",
    config=BigQueryLoggerConfig(
        enabled=True,
        batch_size=1,              # ⚡ Sub-second streaming
        shutdown_timeout=5.0,
        auto_schema_upgrade=True,  # Automatically upgrades BigQuery schema
        create_views=True,         # Automatically creates standard SQL analytics views
        view_prefix="v_adk_official",
        # 🏷️ Customer Strategic & SAP Policy Tags:
        custom_tags={
            "cost_center": "18207041",
            "app_code": "cds-34242",
            "owner": "comercial",
            "environment": "prod",
            "qualificado_como": "Receita",
            "valor": "Alto",
            "criticidade": "sim",
            "it_core": "nao",
            "equipe_do_servico": "squad_vendas",
            "gerencia_responsavel": "gerencia_comercial",
            "business_owner": "lucia_mendes"
        }
    )
)

# 3. Attach Plugin to Runner
runner = InMemoryRunner(agent=agent, plugins=[plugin])

# 4. Execute Multi-Turn Reasoning
async def main():
    events = await runner.run_debug("Consulte o CNPJ 33.000.111/0001-99 e elabore a proposta.")
    await runner.close()

asyncio.run(main())
```

### ✅ Pros:
- **Zero Boilerplate**: Automatically extracts tokens, candidate counts, thinking tokens (`thoughts_token_count`), latencies, and tool arguments without writing manual extraction logic.
- **Deep Agentic Telemetry**: Captures tool inputs, tool execution outputs, errors, and multi-turn conversational traces.
- **Sub-Second Latency**: Uses the high-performance gRPC BigQuery Storage Write API.
- **Built-in Governance**: `custom_tags` guarantees every event emitted by the agent carries SAP and Strategic labels.
- **Automated Views**: Generates ready-to-use analytical views in BigQuery upon initialization.

### ❌ Cons:
- Coupled to the Google ADK framework (`google-adk`). If a team uses raw REST calls or non-ADK architectures, they need standard SDK wrappers.

---

## 🔍 Option 2: Direct BigQuery Streaming API (`google-cloud-bigquery`)

### 🧠 How It Works
Your application makes direct calls to Vertex AI via `google-genai` or `vertexai`, extracts the `usage_metadata` from the response object, and immediately flushes the telemetry row into BigQuery using `bq_client.insert_rows_json()`.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        OPTION 2: DIRECT BIGQUERY STREAMING SDK                         │
│                                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │  Custom Application (FastAPI / Cloud Run / LangChain / LlamaIndex / Python API)  │  │
│  │                                                                                  │  │
│  │  1. Response = client.models.generate_content(...)                                │  │
│  │  2. Usage = response.usage_metadata                                              │  │
│  │  3. bq_client.insert_rows_json(table, [row])                                     │  │
│  └──────────────────────────────────────────┬───────────────────────────────────────┘  │
│                                             │                                          │
│                                             ▼  (Sub-second HTTP REST Streaming)        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                 Google Cloud BigQuery (`genai_finops_governance`)                │  │
│  │  • Table: `agent_events`                                                         │  │
│  │  • Unified Views: `v_genai_governance_dashboard`, `v_value_transformation...`    │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 💻 Production Code Implementation

```python
import time
import datetime
import uuid
from google import genai
from google.cloud import bigquery

# 1. Initialize Clients
vertex_client = genai.Client(vertexai=True, project="aleorg-dev-workload-01", location="us-central1")
bq_client = bigquery.Client(project="aleorg-dev-workload-01")
TABLE_REF = "aleorg-dev-workload-01.genai_finops_governance.agent_events"

# 2. Execute Vertex AI Call
start_t = time.time()
response = vertex_client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Elabore um resumo do procedimento operacional da subestação SE-BAIXADA-01."
)
latency_ms = int((time.time() - start_t) * 1000)

# 3. Extract Genuine Usage Metadata
usage = response.usage_metadata
prompt_tok = usage.prompt_token_count
out_tok = usage.candidates_token_count
total_tok = usage.total_token_count

# 4. Stream Telemetry Row to BigQuery
row = {
    "trace_id": f"trace_{int(time.time())}_{uuid.uuid4().hex[:6]}",
    "span_id": f"span_{uuid.uuid4().hex[:6]}",
    "parent_span_id": None,
    "event_type": "LLM_RESPONSE",
    "timestamp": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    "session_id": f"sess_{int(time.time())}",
    "turn_number": 1,
    "agent_name": "Agent-Operacao",
    "model_name": "gemini-2.5-flash",
    "user_id": "jesus@light.com.br",
    
    # 🏷️ Strategic & SAP Policy Tags:
    "qualificado_como": "Core",
    "valor": "Baixo",
    "budget_usd": 10000.0,
    "token_errors": 0,
    "cost_center": 18207115,
    "app_code": "cds-91023",
    "app_name": "scada_grid_ops",
    "owner": "sistemas",
    "environment": "prod",
    "criticidade": "sim",
    "it_core": "sim",
    "equipe_do_servico": "squad_alta_tensao",
    "gerencia_responsavel": "gerencia_de_operacoes",
    "business_owner": "jesus_rodriguez",

    # 🔢 Real Metrics:
    "prompt_tokens": prompt_tok,
    "cached_tokens": 0,
    "output_tokens": out_tok,
    "total_tokens": total_tok,
    "latency_ms": float(latency_ms),
    "status": "SUCCESS",
    "tool_name": None
}

# ⚡ Sub-second Streaming
errors = bq_client.insert_rows_json(TABLE_REF, [row])
```

### ✅ Pros:
- **Universal Compatibility**: Works in any Python service, microservice (Cloud Run, GKE, Cloud Functions), framework (LangChain, LlamaIndex, Semantic Kernel, custom scripts).
- **Sub-Second Availability**: Rows are queryable in BigQuery and visible in Looker Studio instantly.
- **Granular Control**: Full freedom to customize every field, calculate instant cost estimates, and handle retries.

### ❌ Cons:
- Requires adding BigQuery client calls in your application code or middleware.

---

## 🔍 Option 3: Cloud Logging Log Router Sink (Decoupled Logging)

### 🧠 How It Works
The application writes structured JSON logs using standard Python `logging`. A **Google Cloud Logging Log Router Sink** intercepts these logs and routes them asynchronously to the BigQuery dataset.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        OPTION 3: CLOUD LOGGING LOG ROUTER SINK                         │
│                                                                                        │
│  ┌────────────────────────────────────────┐                                            │
│  │   Application / FinOps Wrapper         │                                            │
│  │   logger.info(json.dumps(telemetry))   │                                            │
│  └──────────────────┬─────────────────────┘                                            │
│                     │                                                                  │
│                     ▼  (Standard stdout / Cloud Logging)                               │
│  ┌────────────────────────────────────────┐                                            │
│  │      Google Cloud Logging              │                                            │
│  └──────────────────┬─────────────────────┘                                            │
│                     │                                                                  │
│                     ▼  (Log Router Sink Filter: `logName:finops_ai_governance`)        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                 Google Cloud BigQuery (`genai_finops_governance`)                │  │
│  │  • Destination Table: `cloud_logging_events`                                     │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 💻 Production Code Implementation

```python
import json
import logging
import time
import google.cloud.logging

# 1. Setup Cloud Logging
log_client = google.cloud.logging.Client()
log_client.setup_logging()
logger = logging.getLogger("finops_ai_governance")

# 2. After LLM Call, emit structured log
telemetry_record = {
    "event_type": "LLM_RESPONSE",
    "model": "gemini-2.5-pro",
    "session_id": "sess_102938",
    "agent_name": "Agent-Juridico",
    "latency_ms": 3210.0,
    "usageMetadata": {
        "promptTokenCount": 2480,
        "candidatesTokenCount": 420,
        "totalTokenCount": 2900
    },
    "customLabels": {
        "cost_center": "18206922",
        "app_code": "cds-77211",
        "qualificado_como": "Transformacional",
        "valor": "Alto",
        "user_id": "evandro@light.com.br"
    }
}

# 3. Emits instantly to stdout / Cloud Logging
logger.info(json.dumps(telemetry_record))
```

### 🛠️ Cloud Logging Sink Setup Command
```bash
gcloud logging sinks create finops_bq_sink \
    bigquery.googleapis.com/projects/aleorg-dev-workload-01/datasets/genai_finops_governance \
    --log-filter='logName:"finops_ai_governance"' \
    --use-partitioned-tables
```

### ✅ Pros:
- **Decoupled Architecture**: Application code never interacts with BigQuery APIs or credentials—it only logs JSON.
- **Zero App Latency Impact**: Logging calls return instantly; BigQuery ingestion happens asynchronously in Google infrastructure.
- **Resilience**: If BigQuery experiences temporary quota issues, Cloud Logging buffers logs without failing user requests.

### ❌ Cons:
- **Ingestion Delay**: Takes 2 to 10 seconds for logs to route and appear in BigQuery tables.
- Requires parsing JSON payloads (`jsonPayload.usageMetadata...`) in BigQuery SQL views.

---

## 🔍 Option 4: Batch Loading (`bq load` / Google Cloud Storage)

### 🧠 How It Works
Application workloads or batch evaluation scripts write telemetry events to local `.jsonl` or `.parquet` files. A scheduled batch job or CLI loads the files into BigQuery.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        OPTION 4: BATCH LOADING (JSONL / GCS)                           │
│                                                                                        │
│  ┌────────────────────────────────────────┐                                            │
│  │   Batch Ingestion Script / Eval Loop   │                                            │
│  │   Writes records to `events.jsonl`     │                                            │
│  └──────────────────┬─────────────────────┘                                            │
│                     │                                                                  │
│                     ▼                                                                  │
│  ┌────────────────────────────────────────┐                                            │
│  │   Google Cloud Storage (GCS Bucket)    │                                            │
│  └──────────────────┬─────────────────────┘                                            │
│                     │                                                                  │
│                     ▼  (bq load --source_format=NEWLINE_DELIMITED_JSON)                │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                 Google Cloud BigQuery (`genai_finops_governance`)                │  │
│  │  • Destination Table: `agent_events`                                             │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 💻 Production Code Implementation

```bash
# Append local batch JSONL to BigQuery:
bq --project_id=aleorg-dev-workload-01 load \
    --noreplace \
    --autodetect \
    --source_format=NEWLINE_DELIMITED_JSON \
    genai_finops_governance.agent_events \
    bigquery/real_live_events.jsonl
```

### ✅ Pros:
- **Free BigQuery Ingestion**: Batch load jobs are completely free of charge in BigQuery (no streaming insert fees).
- Ideal for nightly model evaluation benchmarks, dataset backfills, and offline audits.

### ❌ Cons:
- **Not Real-Time**: Data only appears when the batch job executes (5s to several minutes).
- Not suitable for real-time live interactive dashboards.

---

## 🎯 Strategic Decision Framework: Which Option to Recommend?

```
                                    WHAT IS YOUR WORKLOAD TYPE?
                                                 │
                   ┌─────────────────────────────┴─────────────────────────────┐
                   ▼                                                           ▼
         Are you building AI Agents                               Are you running Custom Microservices,
            with Google ADK?                                          APIs, or Existing Code?
                   │                                                           │
                   ▼                                                           ▼
         ┌───────────────────┐                                       What is your latency
         │   USE OPTION 1    │                                           requirement?
         │  (Official ADK    │                                                 │
         │  BigQuery Plugin) │                               ┌─────────────────┴─────────────────┐
         └───────────────────┘                               ▼                                   ▼
                                                   Sub-Second Real-Time                 Decoupled Logging
                                                  Looker Studio Dashboard                 Audit Pipeline
                                                             │                                   │
                                                             ▼                                   ▼
                                                   ┌───────────────────┐               ┌───────────────────┐
                                                   │   USE OPTION 2    │               │   USE OPTION 3    │
                                                   │  (Direct BigQuery │               │  (Cloud Logging   │
                                                   │   Streaming SDK)  │               │    Router Sink)   │
                                                   └───────────────────┘               └───────────────────┘
```

---

## 📈 Unification in Looker Studio

Regardless of which ingestion method you implement, all telemetry converges into the **Standard BigQuery Governance Schema**:

```sql
SELECT 
    agent_name,
    user_id,
    qualificado_como,  -- Strategic Value Category (Receita, Transformacional, Core)
    valor,             -- Value Tier (Alto vs Baixo)
    budget_usd,        -- Department Budget
    cost_center,       -- SAP ERP Cost Center (18207041, 18206922, etc.)
    app_code,          -- Corporate CMDB Application Code
    model_name,        -- gemini-2.5-pro, gemini-2.5-flash, etc.
    tool_name,         -- Autonomous Function Calls
    prompt_tokens,     -- Real Input Tokens
    output_tokens,     -- Real Candidate Tokens
    total_tokens,      -- Total Tokens (including Thinking Tokens)
    latency_ms,        -- Roundtrip Latency (ms)
    estimated_cost_usd -- Financial Chargeback Cost
FROM `aleorg-dev-workload-01.genai_finops_governance.v_genai_governance_dashboard`
```

This ensures that the **Executive Looker Studio Cockpit** remains **100% unified, consistent, and audit-ready across all teams and architectures**.

---

## 📚 Official Google Cloud Documentation & Latency References

For enterprise architectural reviews and compliance audits, here are the official Google Cloud documentation sources, architecture whitepapers, and service specifications validating these latency metrics:

### 1. BigQuery Storage Write API (Option 1 — ADK Plugin)
* **Official Documentation:** [Google Cloud — BigQuery Storage Write API Overview](https://cloud.google.com/bigquery/docs/write-api)
* **Official ADK Integration:** [Google ADK — BigQuery Agent Analytics Integration](https://adk.dev/integrations/bigquery-agent-analytics/)
* **Official Excerpt:**
  > *"The Storage Write API provides streaming ingestion with robust delivery semantics... When you write to the default stream, records are committed immediately and are queryable as soon as the write request is acknowledged."*
* **Technical Mechanism:** Streams binary Protocol Buffers (protobuf) over bidirectional **gRPC channels (HTTP/2)** directly to BigQuery's Borg workers, achieving sub-second acknowledgment latency (< 100ms - 500ms network round-trip).

---

### 2. BigQuery Streaming API (`insert_rows_json`) (Option 2 — Direct SDK)
* **Official Documentation:** [Google Cloud — Streaming Data into BigQuery](https://cloud.google.com/bigquery/docs/streaming-data-into-bigquery)
* **Official SLA Reference:** [Google Cloud — BigQuery Service Level Agreement (SLA)](https://cloud.google.com/bigquery/sla)
* **Official Excerpt:**
  > *"Data is available for real-time analysis immediately after it is streamed into BigQuery. Streamed data is written to an in-memory streaming buffer and is queryable without delay."*
* **Technical Mechanism:** Individual rows are committed synchronously in the HTTP `tabledata.insertAll` REST request. As soon as the client receives HTTP `200 OK`, the row is immediately accessible to any standard SQL query or Looker Studio refresh.

---

### 3. Cloud Logging Log Router Sink (Option 3 — Decoupled Logging)
* **Official Documentation:** [Google Cloud Logging — Overview of Logs Routing](https://cloud.google.com/logging/docs/routing/overview)
* **BigQuery Sink Guide:** [Google Cloud Logging — Route Logs to BigQuery](https://cloud.google.com/logging/docs/routing/bigquery)
* **Official Excerpt:**
  > *"The Log Router routes log entries to supported destinations as they arrive... Cloud Logging uses streaming inserts to deliver log entries to destination BigQuery tables in near real time."*
* **Technical Mechanism:** Cloud Logging accepts log entries asynchronously into its ingestion buffer and dispatches them to the configured Log Sink. The async queuing and batch dispatch introduce a normal end-to-end propagation latency of **2 to 10 seconds**.

---

### 4. BigQuery Batch Load Jobs (Option 4 — `bq load` / GCS)
* **Official Documentation:** [Google Cloud — Batch Loading Data Overview](https://cloud.google.com/bigquery/docs/batch-loading-data)
* **Quotas & Limits:** [Google Cloud — BigQuery Load Job Quotas](https://cloud.google.com/bigquery/docs/loading-data#quotas_and_limits)
* **Official Excerpt:**
  > *"Loading data into BigQuery using load jobs is asynchronous. When you run a load job, BigQuery creates a job resource and executes the load in the background."*
* **Technical Mechanism:** A batch load job requires initializing a Job resource, scheduling slot capacity in BigQuery's shared query engine, reading source files (JSONL/Parquet), parsing schemas, and writing columnar Capacitor files to Colossus storage. The minimum initialization and commit overhead for any load job is **5 to 15 seconds**, scaling upward with file size.
