# 🔍 Vertex AI Search & RAG Grounding Governance

**Audience:** Data Engineers, Solution Architects, FinOps Teams  
**Purpose:** Cost modeling, metrics tracking, and governance best practices for **Vertex AI Search (Discovery Engine)**, document data stores, and LLM Grounding.

---

## 📋 1. Vertex AI Search Cost Drivers

Vertex AI Search pricing is determined by three distinct components:

| Pricing Dimension | Description | Pricing Model | Optimization Levers |
| :--- | :--- | :--- | :--- |
| **Search Queries** | Standard Search vs. Generative Summarization queries. | **$5.00 per 1,000 queries** (Enterprise Search with LLM Answers) | Client-side query caching, session debouncing. |
| **Document Indexing & Storage** | Volume of indexed PDFs, HTML, BigQuery records, or Cloud Storage buckets. | Charged per GB / Document Units per month. | Purging obsolete versions, chunk size tuning. |
| **Grounding Calls (Vertex AI LLM)** | Gemini calls grounded with Enterprise Search data stores. | Query cost + standard prompt/output token pricing. | Limit top-k chunks returned per search (e.g. k=3 instead of k=10). |

---

## 🗄️ 2. Telemetry Extraction via Cloud Logging

Cloud Logging captures every search query event from Discovery Engine:

```json
{
  "resource": {
    "type": "discoveryengine.googleapis.com/DataStore",
    "labels": {
      "data_store_id": "light-technical-manuals-ds",
      "project_id": "light-attendance-prod-80781068"
    }
  },
  "jsonPayload": {
    "query": "Como restabelecer alimentador de media tensao?",
    "summarySpec": { "summaryResultCount": 3 },
    "latencyMs": 420.5,
    "user": "antonio_lameirao",
    "app_code": "cds-34199"
  }
}
```

---

## 📊 3. BigQuery SQL Analysis for Search Economics

```sql
SELECT 
  DATE(timestamp) AS search_date,
  resource.labels.project_id AS project_id,
  JSON_VALUE(jsonPayload.data_store_id) AS data_store,
  JSON_VALUE(jsonPayload.user) AS user_id,
  COUNT(1) AS total_queries,
  COUNT(1) * 0.005 AS estimated_query_cost_usd,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.latencyMs) AS FLOAT64)), 1) AS avg_latency_ms
FROM `genai_finops_governance.vertex_search_logs`
GROUP BY search_date, project_id, data_store, user_id
ORDER BY total_queries DESC;
```
