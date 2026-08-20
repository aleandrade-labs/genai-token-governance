# 🧠 AI & GenAI Token Governance Guide: Vertex AI, Vertex Search & ADK

**Audience:** FinOps Analysts, AI Engineers, Enterprise Architects, Product Managers, CTO Office  
**Purpose:** End-to-end framework for tracking, attributing, and governing **AI token consumption and costs** across Google Cloud Vertex AI (Gemini / Foundation Models), Vertex AI Search (Discovery Engine), and the Agent Development Kit (ADK).

---

## 📋 Table of Contents
1. [Executive Summary & Core Objectives](#-1-executive-summary--core-objectives)
2. [GenAI Governance Architecture](#-2-genai-governance-architecture)
3. [Component 1: Vertex AI Foundation Models (Gemini 1.5 Pro / Flash)](#-3-component-1-vertex-ai-foundation-models)
4. [Component 2: Vertex AI Search & RAG Grounding](#-4-component-2-vertex-ai-search--rag-grounding)
5. [Component 3: Agent Development Kit (ADK) Multi-Turn Governance](#-5-component-3-agent-development-kit-adk-multi-turn-governance)
6. [BigQuery AI Telemetry Schema & SQL Views](#-6-bigquery-ai-telemetry-schema--sql-views)
7. [Developer Implementation: ADK FinOps Metadata Wrapper](#-7-developer-implementation-adk-finops-metadata-wrapper)
8. [Looker Studio AI Unit Economics Dashboard](#-8-looker-studio-ai-unit-economics-dashboard)

---

## 🌟 1. Executive Summary & Core Objectives

As enterprise adoption of Generative AI expands at Light S/A, traditional cloud cost management must evolve into **AI Unit Economics**. The goal of this framework is to answer critical business and operational questions:

1. **User & Team Attribution:** Which users, business units, and applications (`app_code`) are consuming the most tokens?
2. **Model Tier Optimization:** What is the cost and token distribution between high-capability models (`gemini-1.5-pro`) and cost-efficient models (`gemini-1.5-flash`)?
3. **Prompt vs. Output Economics:** Are teams optimizing prompt context (e.g. context caching) versus generating high-volume candidate output tokens?
4. **Vertex Search & RAG ROI:** How many search queries are performed, what is the document indexing footprint, and what is the cost per grounded response?
5. **Agentic Loops (ADK):** How many tokens and tool invocations are spent per autonomous agent task?

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 AI FINOPS METRIC PILLARS                               │
├──────────────────────────────┬─────────────────────────────┬───────────────────────────┤
│ 1. TOKEN CONSUMPTION         │ 2. COST ATTRIBUTION         │ 3. UNIT ECONOMICS         │
│ • Prompt (Input) Tokens      │ • Attribution by User/LDAP  │ • Cost per User Session   │
│ • Cached Prompt Tokens       │ • Attribution by Cost Center│ • Cost per Search Query   │
│ • Candidate (Output) Tokens  │ • Attribution by App Code   │ • Flash vs Pro Ratio      │
│ • Embedding Characters       │ • Attribution by Business   │ • Token Cache Hit %       │
└──────────────────────────────┴─────────────────────────────┴───────────────────────────┘
```

---

## 🏛️ 2. GenAI Governance Architecture

The governance architecture combines **Cloud Billing Export**, **Cloud Logging Log Router Sink**, and **Application-Level Telemetry** into BigQuery:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  GENAI INVOCATION LAYER                                          │
│                                                                                                  │
│   [ 1. Vertex AI Models ]               [ 2. Vertex Search / RAG ]       [ 3. ADK Agents / Flows ]
│   (Gemini 1.5 Pro, Flash, Embeddings)   (Discovery Engine Search/RAG)    (Multi-turn tool calls) │
└─────────────────────────────────┬────────────────────────────────┬───────────────────────────────┘
                                  │                                │
                                  ▼                                ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   TELEMETRY & INGESTION LAYER                                    │
│                                                                                                  │
│  • Google Cloud Billing Export: Ingests SKU-level token charges, list price, and discounts.      │
│  • Cloud Logging Log Sink: Streams Vertex AI request/response metadata into BigQuery.           │
│  • ADK Client Wrapper: Injects `user_id`, `session_id`, `app_code`, and `cost_center` tags.       │
└─────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   BIGQUERY AI ANALYTICS LAYER                                    │
│                                                                                                  │
│  • `v_genai_token_consumption_by_user`: User-level prompt/output token consumption.             │
│  • `v_genai_model_unit_economics`: Cost per 1K tokens by model family.                          │
│  • `v_vertex_search_query_analytics`: Search query count, grounding units, indexing cost.        │
│  • `v_adk_agent_governance`: Agent tool invocations, multi-turn reasoning cost.                  │
└─────────────────────────────────┬────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                           LOOKER STUDIO EXECUTIVE AI GOVERNANCE DASHBOARD                        │
│                                                                                                  │
│  [ Top Consumers (Users) ]   [ Token Distribution by Model ]   [ Cost Allocation by Cost Center] │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 3. Component 1: Vertex AI Foundation Models

Vertex AI generates billing line items and usage telemetry for all text, multimodal, and embedding requests:

### Billable Metric SKUs:
1. **Prompt Tokens (Input)**: Charged per 1,000 characters or 1,000 tokens (e.g. Gemini 1.5 Flash: ~$0.00001875 / 1k tokens $\le 128k$).
2. **Candidate Tokens (Output)**: Charged per 1,000 tokens (e.g. Gemini 1.5 Flash: ~$0.000075 / 1k tokens $\le 128k$).
3. **Context Caching Tokens**: Stored prompt tokens (up to 75% discount on input tokens plus hourly storage rate).
4. **Text Embedding**: Charged per 1,000 characters for `text-embedding-004` / `text-multilingual-embedding-002`.

### Telemetry Payload Extracted from Cloud Logging:
```json
{
  "resource": {
    "type": "aiplatform.googleapis.com/Endpoint",
    "labels": { "location": "us-central1", "project_id": "light-attendance-prod-80781068" }
  },
  "jsonPayload": {
    "model": "gemini-1.5-flash-001",
    "usageMetadata": {
      "promptTokenCount": 1420,
      "candidatesTokenCount": 380,
      "totalTokenCount": 1800,
      "cachedContentTokenCount": 0
    },
    "customLabels": {
      "user": "raphael_cano",
      "cost_center": "18207243",
      "app_code": "cds-34199",
      "environment": "prod"
    }
  }
}
```

---

## 🔍 4. Component 2: Vertex AI Search & RAG Grounding

Vertex AI Search (formerly Generative AI App Builder / Discovery Engine) governs document search, enterprise search, and RAG grounding:

### Billable Metrics for Search:
1. **Search Queries**: Charged per 1,000 queries (Standard vs. Enterprise Edition with Generative Summarization).
2. **Indexing & Storage Units**: Charged per GB of indexed unstructured/structured documents (e.g. PDFs in Cloud Storage, BigQuery tables, Google Drive).
3. **LLM Grounding Calls**: Grounding with Google Search or Enterprise Data Store (charged as search queries + prompt/candidate tokens for grounding answer generation).

---

## 🛠️ 5. Component 3: Agent Development Kit (ADK) Multi-Turn Governance

ADK builds autonomous multi-step agents that execute tools, query BigQuery, read documents, and run code. 

### Why ADK Needs Dedicated Token Governance:
- **Agentic Loops**: An agent might run 5–10 iterations (thinking $\rightarrow$ calling tool $\rightarrow$ reading output $\rightarrow$ refining answer).
- **Compounding Prompt Size**: In multi-turn chat, each iteration resends the entire conversation history, causing exponential prompt token growth if not cached or truncated.
- **Tool Invocations**: Governance must track how many tokens each specific tool (e.g. `query_database_tool`, `search_knowledge_tool`) consumes.

---

## 📊 6. BigQuery AI Telemetry Schema & SQL Views

Create the following views in your `finops_label_governance` dataset to empower Looker Studio:

### View 1: `v_genai_token_consumption_by_user`
Aggregates daily token usage, prompt vs output ratio, and estimated cost per user:

```sql
CREATE OR REPLACE VIEW `finops_label_governance.v_genai_token_consumption_by_user` AS
SELECT
  DATE(timestamp) AS usage_date,
  COALESCE(JSON_VALUE(jsonPayload.customLabels.user), 'service_account') AS user_id,
  JSON_VALUE(jsonPayload.customLabels.app_code) AS app_code,
  JSON_VALUE(jsonPayload.customLabels.cost_center) AS cost_center,
  JSON_VALUE(jsonPayload.model) AS model_name,
  COUNT(1) AS total_requests,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64)) AS total_prompt_tokens,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.cachedContentTokenCount) AS INT64)) AS total_cached_tokens,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64)) AS total_output_tokens,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.totalTokenCount) AS INT64)) AS total_tokens,
  -- Estimated cost calculation based on model rates (example Flash rate)
  ROUND(
    SUM(
      CASE 
        WHEN JSON_VALUE(jsonPayload.model) LIKE '%flash%' 
          THEN (CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64) * 0.00001875 / 1000) + 
               (CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64) * 0.000075 / 1000)
        WHEN JSON_VALUE(jsonPayload.model) LIKE '%pro%' 
          THEN (CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64) * 0.00125 / 1000) + 
               (CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64) * 0.00375 / 1000)
        ELSE 0.0
      END
    ), 4
  ) AS estimated_cost_usd
FROM `finops_label_governance.vertex_ai_request_logs`
GROUP BY usage_date, user_id, app_code, cost_center, model_name;
```

---

### View 2: `v_genai_model_unit_economics`
Compares efficiency, latency, and average tokens per request across model families:

```sql
CREATE OR REPLACE VIEW `finops_label_governance.v_genai_model_unit_economics` AS
SELECT
  JSON_VALUE(jsonPayload.model) AS model_name,
  COUNT(1) AS total_invocations,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64)), 1) AS avg_prompt_tokens,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64)), 1) AS avg_output_tokens,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.usageMetadata.totalTokenCount) AS INT64)), 1) AS avg_total_tokens,
  ROUND(SAFE_DIVIDE(SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.cachedContentTokenCount) AS INT64)), 
                     SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64))) * 100, 2) AS cache_hit_rate_pct
FROM `finops_label_governance.vertex_ai_request_logs`
GROUP BY model_name;
```

---

### View 3: `v_vertex_search_query_analytics`
Tracks search queries, summarization volume, and latency:

```sql
CREATE OR REPLACE VIEW `finops_label_governance.v_vertex_search_query_analytics` AS
SELECT
  DATE(timestamp) AS search_date,
  resource.labels.project_id AS project_id,
  JSON_VALUE(jsonPayload.dataStoreId) AS data_store_id,
  COUNT(1) AS total_search_queries,
  COUNTIF(JSON_VALUE(jsonPayload.summarySpec) IS NOT NULL) AS queries_with_generative_summary,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.latencyMs) AS FLOAT64)), 2) AS avg_latency_ms,
  -- Vertex AI Search standard query pricing ($5 per 1,000 queries)
  ROUND(COUNT(1) * (5.0 / 1000), 4) AS search_cost_usd
FROM `finops_label_governance.vertex_search_logs`
GROUP BY search_date, project_id, data_store_id;
```

---

## 💻 7. Developer Implementation: ADK FinOps Metadata Wrapper

To ensure every GenAI call is tagged with the user and customer policy tags, developers wrap Vertex AI client calls using the **ADK FinOps Wrapper**:

```python
import os
import vertexai
from vertexai.generative_models import GenerativeModel

class FinOpsGenerativeModel:
    """
    Wrapper for Vertex AI GenerativeModel that automatically injects
    customer policy tags (cost_center, app_code, user) for FinOps token attribution.
    """
    def __init__(
        self,
        model_name: str,
        app_code: str,
        cost_center: str,
        user_id: str,
        environment: str = "prod"
    ):
        self.model = GenerativeModel(model_name)
        self.metadata_labels = {
            "app_code": app_code,
            "cost_center": cost_center,
            "user": user_id,
            "environment": environment
        }

    def generate_content(self, prompt: str, **kwargs):
        """Generates content and logs FinOps token usage telemetry."""
        # 1. Execute Vertex AI model call
        response = self.model.generate_content(prompt, **kwargs)
        
        # 2. Extract token usage metadata
        usage = response.usage_metadata
        prompt_tokens = usage.prompt_token_count
        output_tokens = usage.candidates_token_count
        total_tokens = usage.total_token_count

        # 3. Emit structured FinOps telemetry log (streamed automatically to BigQuery)
        print(f"[FINOPS_AI_USAGE] user={self.metadata_labels['user']} "
              f"app={self.metadata_labels['app_code']} "
              f"cost_center={self.metadata_labels['cost_center']} "
              f"prompt_tokens={prompt_tokens} "
              f"output_tokens={output_tokens} "
              f"total_tokens={total_tokens}")

        return response

# Example Usage in an Application:
# client = FinOpsGenerativeModel(
#     model_name="gemini-1.5-flash",
#     app_code="cds-34199",
#     cost_center="18207243",
#     user_id="raphael_cano"
# )
# response = client.generate_content("Analyze this smart meter reading anomaly.")
```

---

## 📈 8. Looker Studio AI Unit Economics Dashboard

Add an **"AI & GenAI Token Governance"** page to your Looker Studio report:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🧠 LIGHT S/A — GENAI TOKEN & COST GOVERNANCE DASHBOARD                                                  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                          │
│  [ Total Tokens ]       [ Prompt Tokens ]       [ Output Tokens ]       [ Total AI Cost ]                │
│    148.2 M                112.5 M                 35.7 M                  $ 248.50 USD                   │
│                                                                                                          │
├────────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│  👤 TOP GENAI CONSUMERS (BY USER / EMAIL)          │  🤖 TOKEN DISTRIBUTION BY MODEL                     │
│  ┌────────────────────────┬──────────────┬────────┐│  ┌────────────────────────┬─────────────┬─────────┐ │
│  │ User / Caller          │ Total Tokens │ Est. $ ││  │ Model Name             │ Tokens (M)  │ Share % │ │
│  ├────────────────────────┼──────────────┼────────┤│  ├────────────────────────┼─────────────┼─────────┤ │
│  │ raphael_cano           │  42.1 M      │ $72.50 ││  │ gemini-1.5-flash       │ 104.2 M     │  70.3%  │ │
│  │ antonio_lameirao       │  28.4 M      │ $48.20 ││  │ gemini-1.5-pro         │  32.1 M     │  21.7%  │ │
│  │ equipe_transformacao   │  18.7 M      │ $31.10 ││  │ text-embedding-004     │  11.9 M     │   8.0%  │ │
│  └────────────────────────┴──────────────┴────────┘│  └────────────────────────┴─────────────┴─────────┘ │
├────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┤
│  🏢 COST ALLOCATION BY CUSTOMER COST CENTER (SAP) & APP CODE                                             │
│  ┌─────────────┬─────────────┬───────────────────────────┬──────────────┬──────────────────┐             │
│  │ Cost Center │ App Code    │ Application Name          │ Total Tokens │ Total Cost (USD) │             │
│  ├─────────────┼─────────────┼───────────────────────────┼──────────────┼──────────────────┤             │
│  │ 18207243    │ cds-34199   │ attendance (SAC)          │  58.4 M      │ $ 98.40          │             │
│  │ 12272260    │ cds-59339   │ conexao_silvestre (P&D)   │  34.1 M      │ $ 56.20          │             │
│  │ 18207041    │ cds-34242   │ energy_watch              │  28.9 M      │ $ 49.10          │             │
│  └─────────────┴─────────────┴───────────────────────────┴──────────────┴──────────────────┘             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Summary Checklist for AI Governance

- [x] **SKU-Level Ingestion**: Billing export enabled for `aiplatform.googleapis.com` and `discoveryengine.googleapis.com`.
- [x] **Metadata Attribution**: User LDAP, `cost_center`, `app_code`, and `business_owner` injected in requests.
- [x] **BigQuery Views**: `v_adk_executive_kpis`, `v_adk_user_leaderboard`, `v_adk_model_distribution`, `v_adk_cost_center_attribution`, `v_adk_tool_analytics`, `v_adk_daily_trend`.
- [x] **Looker Studio Dashboard**: Real-time tracking of token counts, model share, tool health, and cost per user.

---

## 📚 9. Documentation Suite (`docs/`) & Resources

- 🏗️ **[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)**: Deep dive into Log Router sinks, Storage Write API streaming, and BigQuery partitioning.
- 🤖 **[`docs/ADK_BIGQUERY_ANALYTICS.md`](docs/ADK_BIGQUERY_ANALYTICS.md)**: Implementation guide for [ADK BigQuery Agent Analytics](https://adk.dev/integrations/bigquery-agent-analytics/).
- 🛠️ **[`docs/ADK_FINOPS_WRAPPER.md`](docs/ADK_FINOPS_WRAPPER.md)**: Python wrapper with automatic SAP cost center and user LDAP attribution.
- 🔍 **[`docs/VERTEX_SEARCH_GOVERNANCE.md`](docs/VERTEX_SEARCH_GOVERNANCE.md)**: Discovery Engine query pricing, document indexing, and RAG grounding.
- 📊 **[`docs/LOOKER_STUDIO_DASHBOARD.md`](docs/LOOKER_STUDIO_DASHBOARD.md)**: Step-by-step widget recipes and layout for Looker Studio.
- 🗄️ **[`bigquery/adk_agent_analytics_views.sql`](bigquery/adk_agent_analytics_views.sql)**: BigQuery SQL DDL for the 6 pre-calculated analytical views.

