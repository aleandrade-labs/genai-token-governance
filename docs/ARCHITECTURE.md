# 🏗️ GenAI Token Governance & Telemetry Architecture

**Audience:** Cloud Architects, AI Platform Engineers, FinOps Specialists  
**Scope:** Technical architecture for telemetry ingestion, log routing, BigQuery analytical modeling, and real-time dashboarding for Generative AI on Google Cloud.

---

## 🏛️ End-to-End System Architecture

<p align="center">
  <img src="architecture_genai_governance.svg" alt="Google Cloud FinOps — GenAI Token & Cost Governance Architecture" width="100%" />
</p>

---

## 🔍 1. Ingestion Mechanisms

To provide complete cost and token attribution without adding latency or breaking developer workflows, telemetry is captured through direct Google ADK integration:

### Stream A: Official Google ADK BigQuery Analytics (`BigQueryAgentAnalyticsPlugin`)
The [Google Agent Development Kit (ADK)](https://adk.dev) provides native telemetry streaming via `BigQueryAgentAnalyticsPlugin`. The plugin uses the high-throughput **BigQuery Storage Write API (gRPC)** to stream every multi-turn prompt, candidate token count, latency measurement, and autonomous tool call in **sub-second real time (< 1s)**.
- **Table Destination:** `genai_finops_governance.adk_events` & `agent_events`
- **Authentication:** Google Cloud Application Default Credentials (ADC) with Quota Project enforcement (`Zero API Keys`).
- **Telemetry Emitted:** `prompt_token_count`, `candidates_token_count`, `total_token_count`, `latency_ms`, `tool_invocations`, `caller_user_id`, `cost_center`, `application_code`.

### Stream B: Vertex AI Model Garden Dispatch
Direct calls to Gemini 1.5 Flash, Gemini 1.5 Pro, and Gemini 2.0 automatically produce structured token usage metadata that is ingested and matched to enterprise Cost Centers (`SAP 18207243`, `18207244`, `18207245`).

---

## 🗄️ 2. BigQuery Data Modeling Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    BigQuery AI Dataset                      │
│                `genai_finops_governance`                    │
├──────────────────────────────┬──────────────────────────────┤
│ RAW TELEMETRY TABLES         │ 6 ANALYTICAL SQL VIEWS       │
│ • `agent_events` (Looker BI) │ • `v_adk_executive_kpis`     │
│ • `adk_events` (ADK Plugin)  │ • `v_adk_user_leaderboard`   │
│                              │ • `v_adk_model_distribution` │
│                              │ • `v_adk_cost_center_attrib` │
│                              │ • `v_adk_tool_analytics`     │
│                              │ • `v_adk_daily_trend`        │
└──────────────────────────────┴──────────────────────────────┘
```

1. **Partitioning**: All raw tables are partitioned by `DATE(timestamp)` with 90-day retention to guarantee minimal storage cost.
2. **Clustering**: Tables are clustered by `user_id`, `cost_center`, `application_code`, and `model_name` for millisecond Looker Studio query speeds.
3. **Views**: Analytical views abstract JSON parsing, compute token cost formulas ($0.075 / $0.30 per 1M tokens), and calculate prompt vs. output ratios in real time.
