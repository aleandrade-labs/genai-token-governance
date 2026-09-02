# 🧠 GenAI Token & Cost Governance with Official Google ADK

[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com)
[![Google ADK](https://img.shields.io/badge/Google_ADK-2.7.1-34A853?style=for-the-badge&logo=google&logoColor=white)](https://adk.dev)
[![Vertex AI](https://img.shields.io/badge/Vertex_AI-Gemini_2.5-EA4335?style=for-the-badge&logo=google&logoColor=white)](https://cloud.google.com/vertex-ai)
[![BigQuery](https://img.shields.io/badge/BigQuery-Storage_Write_API-669DF6?style=for-the-badge&logo=google-bigquery&logoColor=white)](https://cloud.google.com/bigquery)
[![Looker Studio](https://img.shields.io/badge/Looker_Studio-Real_Time_BI-FBBC04?style=for-the-badge&logo=google&logoColor=white)](https://lookerstudio.google.com)

**Enterprise Engagement:** Google Cloud PSO — FinOps & GenAI Governance  
**Environment:** Argolis (`aleorg-dev-workload-01` | Org ID: `1068294623135`)  
**Official Reference:** [Google Agent Development Kit (ADK) — BigQuery Agent Analytics](https://adk.dev/integrations/bigquery-agent-analytics/)

---

## 📋 Table of Contents
1. [Executive Overview & Value Proposition](#-1-executive-overview--value-proposition)
2. [End-to-End Architecture](#-2-end-to-end-architecture)
3. [Real-Time Storage Write API vs. Billing Latency](#-3-real-time-storage-write-api-vs-billing-latency)
4. [Quickstart: Setup & Prerequisites](#-4-quickstart-setup--prerequisites)
5. [Live Vertex AI Token Generation Suite](#-5-live-vertex-ai-token-generation-suite)
6. [Interactive Terminal AI Assistant](#-6-interactive-terminal-ai-assistant)
7. [Official Google ADK Multi-Agent Execution](#-7-official-google-adk-multi-agent-execution)
8. [How to Erase / Reset BigQuery Data](#-8-how-to-erase--reset-bigquery-data)
9. [BigQuery Schema & Analytical Views](#-9-bigquery-schema--analytical-views)
10. [Executive Looker Studio Dashboard Setup](#-10-executive-looker-studio-dashboard-setup)
11. [CLI Command Reference](#-11-cli-command-reference)

---

## 🎯 1. Executive Overview & Value Proposition

As enterprise teams scale Generative AI agents on Google Cloud (Vertex AI Gemini 2.5 Pro / Flash, Claude, Search & RAG), CFOs and FinOps teams face two critical blindspots:
1. **Billing Latency**: Standard Cloud Billing exports take **4 to 24 hours** to settle, preventing real-time anomaly detection.
2. **Missing Token Attribution**: Standard billing shows total Vertex AI cost, but cannot attribute costs to individual **Agent Names**, **Tool Calls**, **SAP Cost Centers**, **Strategic Value Tiers (`valor`)**, or **Business Classification (`qualificado_como`)**.

### The Solution: 100% Real-Time ADK BigQuery Analytics
By integrating the official **`BigQueryAgentAnalyticsPlugin`** from the [Google Agent Development Kit (ADK)](https://adk.dev), every real multi-turn prompt, candidate token, tool invocation, and latency span is streamed **in sub-second real time (< 1s)** directly to BigQuery via the gRPC **BigQuery Storage Write API**, with **Zero API Keys** required (100% IAM & ADC authenticated).

---

## 🏗️ 2. End-to-End Architecture

<p align="center">
  <img src="docs/architecture_genai_governance.svg" alt="Google Cloud FinOps — GenAI Token & Cost Governance Architecture" width="100%" />
</p>

---

## ⚡ 3. Real-Time Storage Write API vs. Billing Latency

| Feature | Standard GCP Cloud Billing Export | Official ADK BigQuery Agent Analytics |
| :--- | :--- | :--- |
| **Ingestion Latency** | **4 to 24 Hours** (Batch reconciliation) | **Sub-Second (< 1000 ms)** (gRPC streaming) |
| **Data Authenticity** | Post-processed billing aggregation | **100% Real Vertex AI `usage_metadata` (Tokens & Latency)** |
| **Granularity** | Project & SKU level aggregated cost | **Per-prompt, per-candidate, per-tool call, per-user** |
| **Tool Calling Telemetry** | ❌ None | ✅ Tool execution duration, status & parameters |
| **Business Categorization** | ❌ None | ✅ `qualificado_como` (Receita, Transformacional, Core) |
| **SAP Cost Center Chargeback**| Requires static project label tags | ✅ Dynamic run-time business attribution |
| **Authentication** | Cloud Billing Admin | **Google Cloud ADC / IAM (Zero API Keys)** |

---

## 🚀 4. Quickstart: Setup & Prerequisites

### Step 1: Clone Repository
```bash
git clone git@github.com:aleandrade-labs/genai-token-governance.git
cd genai-token-governance
```

### Step 2: Create Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Authenticate with Google Cloud ADC (Zero API Keys!)
```bash
gcloud auth application-default login
gcloud auth application-default set-quota-project aleorg-dev-workload-01
gcloud config set project aleorg-dev-workload-01
```

---

## ⚡ 5. Live Vertex AI Token Generation Suite

Execute **100% real API calls** to Vertex AI Gemini 2.5 Flash / Gemini 2.5 Pro across the 11 specialized enterprise agents from the **Light AI Value Transformation** catalog:

```bash
# Execute 1 real live round across all 11 enterprise agents:
.venv/bin/python3 src/run_live_gemini_batch.py

# Execute 3 consecutive real rounds:
.venv/bin/python3 src/run_live_gemini_batch.py --rounds 3

# Force execution on Gemini 2.5 Pro (Deep Reasoning):
.venv/bin/python3 src/run_live_gemini_batch.py --model gemini-2.5-pro
```

### 📋 Enterprise Agents Tested:
- **`Agent-Vendas`** (`lucia@light.com.br`) — **Receita / Alto** (Market ACL Energy Proposals)
- **`Agent-Juridico`** (`evandro@light.com.br`) — **Transformacional / Alto** (ANEEL SLA Contract Compliance)
- **`Agent-RH`** (`victor@light.com.br`) — **Corporativo / Alto** (NR-10 Live-Line Training)
- **`Agent-IT`** (`senna@light.com.br`) — **Corporativo / Alto** (Terraform GKE Private Autopilot)
- **`Agent-Operacao`** (`jesus@light.com.br`) — **Core / Baixo** (138kV Substation SCADA Contingencies)
- **`FinOps-Analyst`** (`lucero_patricia@light.com.br`) — **Corporativo / Alto** (Compute Engine CUD ROI)
- **`Agent-Comunicacao`** (`vicente@light.com.br`) — **Core / Alto** (Press & Institutional Notes)
- **`Agent-Onboarding`** (`jose_carlos@light.com.br`) — **Core / Baixo** (New Employee IT Setup)
- **`Executive-Agent`** (`jorge_sanchez@light.com.br`) — **Core / Alto** (C-Level Board Briefings)
- **`AI-Gov`** (`omar@light.com.br`) — **Core / Alto** (Responsible AI & LGPD Audit)
- **`AI-Agentic`** (`juan@light.com.br`) — **Core / Alto** (Google ADK Multi-Agent Orchestration)

---

## 💬 6. Interactive Terminal AI Assistant

Launch a real-time conversational agent directly in your terminal, fully connected to Vertex AI with tool calling and BigQuery telemetry:

```bash
.venv/bin/python3 src/interactive_chat.py
```

- Type prompts interactively (e.g. *"Qual o status dos alimentadores da Subestação Frei Caneca?"*).
- Switch models on the fly with `/model gemini-2.5-pro`.
- Switch application profiles with `/app substation_copilot`.

---

## 🤖 7. Official Google ADK Multi-Agent Execution

Run the official Google Agent Development Kit (ADK) runtime with autonomous tools and real-time BigQuery streaming:

```bash
# Run single interactive ADK session:
.venv/bin/python3 src/run_official_adk_agent.py

# Run multi-workload batch:
.venv/bin/python3 src/run_official_adk_agent.py --batch
```

---

## 🧹 8. How to Erase / Reset BigQuery Data

### Option A: Via Python CLI Flag (Easiest)
Wipe past telemetry and run a clean real session:
```bash
.venv/bin/python3 src/run_official_adk_agent.py --clear --batch
```

### Option B: Via `bq` CLI Command
```bash
bq query --use_legacy_sql=false "TRUNCATE TABLE aleorg-dev-workload-01.genai_finops_governance.agent_events"
bq query --use_legacy_sql=false "TRUNCATE TABLE aleorg-dev-workload-01.genai_finops_governance.adk_events"
```

---

## 🗄️ 9. BigQuery Schema & Analytical Views

Pre-built SQL views under `aleorg-dev-workload-01.genai_finops_governance`:

| View Name | Purpose | Looker Studio Visualization |
| :--- | :--- | :--- |
| **`v_genai_governance_dashboard`** | Master unified view with all 10 Customer Policy Tags + `qualificado_como` + `valor` | Master Dashboard View |
| **`v_value_transformation_dashboard`** | Strategic value transformation & budget tracking view | Value & Budget Matrix Table |
| **`v_adk_executive_kpis`** | Global tokens, active sessions, tool success %, total USD cost | Header Scorecards |
| **`v_adk_user_leaderboard`** | Consumption ranked by user email, app name, and cost center | User Leaderboard Table |
| **`v_adk_model_distribution`**| Breakdown across Gemini 2.5 Pro, Flash, and 2.0 | Model Family Donut Chart |
| **`v_adk_cost_center_attribution`**| Financial chargeback breakdown by SAP Cost Center | Chargeback Attribution Table |
| **`v_adk_tool_analytics`** | Function calling frequency, latency ms, and error rate | Tool Observability Bar Chart |
| **`v_adk_daily_trend`** | 30-day token volume and cost trajectory | Time Series Line Chart |

---

## 📊 10. Executive Looker Studio Dashboard Setup

Refer to the complete, step-by-step guide:  
👉 **[Looker Studio GenAI & ADK Governance: Complete Click-by-Click Guide](docs/LOOKER_STUDIO_DASHBOARD.md)**

---

## 🛠️ 11. CLI Command Reference

| Command | Purpose |
| :--- | :--- |
| `.venv/bin/python3 src/run_live_gemini_batch.py` | Run 1 real live round across all 11 agents on Vertex AI |
| `.venv/bin/python3 src/run_live_gemini_batch.py --rounds 3` | Run 3 consecutive live rounds on Vertex AI |
| `.venv/bin/python3 src/run_live_gemini_batch.py --model gemini-2.5-pro` | Force Gemini 2.5 Pro reasoning model |
| `.venv/bin/python3 src/run_official_adk_agent.py` | Run live interactive ADK agent with SCADA tools |
| `.venv/bin/python3 src/run_official_adk_agent.py --clear --batch` | Erase past data & run multi-workload batch |
| `.venv/bin/python3 src/interactive_chat.py` | Interactive terminal shell with dynamic model/app switching |
