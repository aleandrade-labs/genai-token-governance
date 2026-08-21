# 📊 Looker Studio GenAI & ADK Governance: Complete Click-by-Click Guide

**Audience:** FinOps Specialists, Cloud Architects, AI Platform Engineers, Executives  
**Goal:** Build the complete **Executive GenAI Token, Cost & Label Governance Dashboard** in Google Looker Studio in **under 5 minutes** with zero coding.

---

## 🎯 What You Will Build

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🧠 GOOGLE CLOUD FINOPS — GENAI & ADK AGENT GOVERNANCE DASHBOARD                                                  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  [ Filter: SAP Cost Center ▼ ]   [ Filter: App Code ▼ ]   [ Filter: Owner ▼ ]   [ Date Range: Last 30 Days 📅 ]  │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                  │
│  [ Total Sessions ]     [ Total Tokens ]      [ Prompt Tokens ]     [ Output Tokens ]     [ Total AI Cost ]      │
│         12                   56.9 K                51.3 K                5.6 K               $ 0.02 USD          │
│                                                                                                                  │
├────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────┤
│  👤 TOP GENAI CONSUMERS (USER LEADERBOARD)             │  🤖 MODEL FAMILY DISTRIBUTION                           │
│  ┌────────────────────────────┬─────────────┬─────────┐│  ┌────────────────────────────┬─────────────┬─────────┐ │
│  │ User / Email               │ Tokens      │ Cost $  ││  │ Model Name                 │ Tokens      │ Share % │ │
│  ├────────────────────────────┼─────────────┼─────────┤│  ├────────────────────────────┼─────────────┼─────────┤ │
│  │ admin@altostrat.com        │    43.1 K   │ $ 0.01  ││  │ gemini-1.5-flash           │   33.0 K    │  58.1%  │ │
│  │ alexandrade@google.com     │     9.3 K   │ $ 0.01  ││  │ gemini-1.5-pro             │   13.1 K    │  23.0%  │ │
│  │ sa-finops-governance...    │     4.4 K   │ $ 0.00  ││  │ gemini-2.0-flash           │   10.8 K    │  18.9%  │ │
│  └────────────────────────────┴─────────────┴─────────┘│  └────────────────────────────┴─────────────┴─────────┘ │
├────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
│  🏢 CONSUMPTION BY COST CENTER (SAP SHARE)             │  ⚡ AUTONOMOUS TOOL INVOCATIONS                          │
│  ┌────────────────────────────┬─────────────┬─────────┐│  ┌────────────────────────────┬─────────────┬─────────┐ │
│  │ SAP Cost Center            │ Tokens      │ Cost $  ││  │ Tool Name                  │ Calls       │ Status  │ │
│  ├────────────────────────────┼─────────────┼─────────┤│  ├────────────────────────────┼─────────────┼─────────┤ │
│  │ 18207041 (energy_watch)    │    30.3 K   │ $ 0.01  ││  │ query_substation_status    │     8       │ 100% OK │ │
│  │ 12272260 (conexao_silvest.)│     9.3 K   │ $ 0.01  ││  │ calculate_feeder_loss      │     1       │ 100% OK │ │
│  │ 18207115 (substation_cop.) │     7.0 K   │ $ 0.00  ││  │ search_customer_history    │     1       │ 100% OK │ │
│  │ 18207243 (attendance_sac)  │     5.9 K   │ $ 0.00  ││  │ query_substation_telemetry │     1       │ 100% OK │ │
│  │ 18206922 (smart_meter_rag) │     4.4 K   │ $ 0.00  ││  │ check_smart_meter_anomaly  │     1       │ 100% OK │ │
│  └────────────────────────────┴─────────────┴─────────┘│  └────────────────────────────┴─────────────┴─────────┘ │
├────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────┤
│  🏢 COMPLETE ENTERPRISE FINANCIAL CHARGEBACK (ALL 10 CUSTOMER POLICY TAGS)                                       │
│  ┌──────────┬───────────┬─────────────────────┬──────┬──────────┬─────────┬────────────────────────┬───────────┐ │
│  │ Cost Ctr │ App Code  │ Application         │ Env  │ Critical │ IT Core │ Gerência Responsável   │ Cost ($)  │ │
│  ├──────────┼───────────┼─────────────────────┼──────┼──────────┼─────────┼────────────────────────┼───────────┤ │
│  │ 18207041 │ cds-34242 │ energy_watch_grid   │ prod │ sim      │ nao     │ gerencia_de_sistemas   │ $ 0.01    │ │
│  │ 12272260 │ cds-59339 │ conexao_silvestre_pd│ prod │ nao      │ nao     │ coord_projetos_pdi     │ $ 0.01    │ │
│  │ 18207115 │ cds-91023 │ substation_copilot  │ prod │ sim      │ sim     │ gerencia_transf_digital│ $ 0.00    │ │
│  │ 18207243 │ cds-34199 │ attendance_sac      │ prod │ nao      │ nao     │ gerencia_transf_digital│ $ 0.00    │ │
│  │ 18206922 │ cds-77211 │ smart_meter_rag     │ prod │ nao      │ nao     │ gerencia_de_sistemas   │ $ 0.00    │ │
│  ├──────────┼───────────┼─────────────────────┼──────┼──────────┼─────────┼────────────────────────┼───────────┤ │
│  │ TOTAL    │           │                     │      │          │         │                        │ $ 0.02    │ │
│  └──────────┴───────────┴─────────────────────┴──────┴──────────┴─────────┴────────────────────────┴───────────┘ │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏷️ Customer Policy Tags Dictionary

The BigQuery views automatically expose all **10 Customer Policy Tags** from the enterprise CSV mapping:

| Field Name | Type | Example Values | Description / Usage |
| :--- | :--- | :--- | :--- |
| **`cost_center`** | `STRING` | `18207041`, `18207243`, `12272260` | SAP ERP Financial Cost Center for billing chargeback |
| **`app_code`** | `STRING` | `cds-34242`, `cds-34199`, `cds-59339` | Internal IT Architecture Application Code |
| **`application`** | `STRING` | `energy_watch`, `attendance`, `conexao_silvestre` | Application / AI workload name |
| **`owner`** | `STRING` | `arquitetura`, `pdi`, `sistemas`, `governanca` | Primary organizational entity / team owner |
| **`environment`** | `STRING` | `prod`, `hml`, `dev` | Deployment environment tier |
| **`criticidade`** | `STRING` | `sim`, `nao` | Mission-critical system indicator |
| **`it_core`** | `STRING` | `sim`, `nao` | Core enterprise electrical grid / IT infrastructure |
| **`equipe_do_servico`** | `STRING` | `pdi-ew`, `equipe_attendance`, `equipe_pdi` | Assigned engineering squad |
| **`gerencia_responsavel`**| `STRING`| `gerencia_de_sistemas`, `gerencia_de_transf_digital` | Executive leadership department |
| **`business_owner`** | `STRING` | `raphael_cano`, `antonio_lameirao`, `alexandrade` | Business stakeholder responsible for budget |

---

## 🗄️ BigQuery Data Source Setup (30 seconds)

1. Open **[https://lookerstudio.google.com/](https://lookerstudio.google.com/)** $\rightarrow$ Click **`+ Create`** $\rightarrow$ **`Report`**.
2. In the **"Add data to report"** popup:
   - Select **`BigQuery`**.
   - **Project**: `aleorg-dev-workload-01`.
   - **Dataset**: `genai_finops_governance`.
   - **Table / View**: **`v_genai_governance_dashboard`** *(Recommended unified view)*.
3. Click **`Add`** $\rightarrow$ Click **`Add to Report`**.
4. Set Theme: Click **`Theme and layout`** on the top toolbar $\rightarrow$ Select **Simple Dark** (or keep Simple Light).

---

## 🔢 Step 1: Top KPI Scorecards

Add 5 scorecards side-by-side across the top row:

| Scorecard # | Metric Field | Aggregation | Display Name | Format / Style |
| :--- | :--- | :--- | :--- | :--- |
| **Card 1** | `total_tokens` | `SUM` | **`Total Tokens`** | Compact Numbers (`56.9K`) |
| **Card 2** | `session_id` | `COUNT_DISTINCT` | **`Total Sessions`** | Decimal Precision: `0` (`12`) |
| **Card 3** | `prompt_tokens` | `SUM` | **`Prompt Tokens`** | Compact Numbers (`51.3K`) |
| **Card 4** | `output_tokens` | `SUM` | **`Output Tokens`** | Compact Numbers (`5.6K`) |
| **Card 5** | `estimated_cost_usd` | `SUM` | **`Total AI Cost`** | Currency: `USD ($)` (`$0.02`) |

---

## 👤 Step 2: User / Consumer Leaderboard Table

1. Click **`Add a chart`** $\rightarrow$ Select **`Table`** (or `Table with heatmap`).
2. **Setup Tab**:
   - **Dimension**: `user_id`
   - **Metrics**: `total_tokens` (SUM), `estimated_cost_usd` (SUM)
   - **Sort**: `total_tokens` $\rightarrow$ `Descending`
3. **Style Tab**:
   - Change `total_tokens` metric format to **`Heatmap`** (Blue bar).

---

## 🤖 Step 3: Model Family Distribution (Donut Chart)

1. Click **`Add a chart`** $\rightarrow$ Select **`Donut chart`**.
2. **Setup Tab**:
   - **Dimension**: `model_name` (e.g. `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash`)
   - **Metric**: `total_tokens` (SUM)
   - **Sort**: `total_tokens` $\rightarrow$ `Descending`
3. **Style Tab**:
   - **Hole radius**: `60%`
   - **Slice label**: `Percentage`

---

## 🏢 Step 4: Cost Center Consumption Views

### Option A: Cost Center Share Donut Chart
* **Add Chart**: `Donut chart`
* **Dimension**: `cost_center`
* **Metric**: `total_tokens` (or `estimated_cost_usd`)
* **Slice Label**: `Percentage`

### Option B: Cost Center by Model Stacked Bar Chart
* **Add Chart**: `Stacked column chart` (or Stacked bar)
* **Dimension**: `cost_center`
* **Breakdown Dimension**: `model_name`
* **Metric**: `total_tokens` (SUM)

---

## ⚡ Step 5: Autonomous Tool Analytics (Bar Chart)

1. Click **`Add a chart`** $\rightarrow$ Select **`Bar chart`** (Horizontal).
2. **Setup Tab**:
   - **Dimension**: `tool_name` (e.g. `query_substation_status`, `calculate_feeder_loss`)
   - **Metric**: `Record Count` (or `latency_ms` AVG)
   - **Filter**: Add filter `event_type = 'TOOL_COMPLETED'`
   - **Sort**: `Record Count` $\rightarrow$ `Descending`

---

## 🏢 Step 6: Complete Policy Tags Financial Chargeback Table

1. Click **`Add a chart`** $\rightarrow$ Select **`Table`**.
2. Place across the bottom width of the canvas.
3. **Setup Tab**:
   - **Dimensions**:
     1. `cost_center` (SAP Cost Center)
     2. `app_code` (Application Code)
     3. `application` (App Name)
     4. `environment` (`prod`, `hml`, `dev`)
     5. `criticidade` (`sim`, `nao`)
     6. `it_core` (`sim`, `nao`)
     7. `gerencia_responsavel` (Department)
     8. `business_owner` (Stakeholder)
   - **Metrics**: 
     - `total_tokens` (SUM)
     - `estimated_cost_usd` (SUM)
   - **Sort**: `total_tokens` $\rightarrow$ `Descending`
   - *(Optional Filter)*: `event_type = 'LLM_RESPONSE'`
4. **Style Tab**:
   - Check **`Show summary row`** (Adds automatic `TOTAL` row showing grand total tokens and cost).

---

## 🎛️ Step 7: Add Interactive Filter Controls

Place dropdown filters across the top banner to enable instant cross-filtering:

1. **SAP Cost Center Filter**: Click **`Add a control`** $\rightarrow$ **`Drop-down list`** $\rightarrow$ Set Control Field to **`cost_center`**.
2. **Application Code Filter**: Add Drop-down list $\rightarrow$ Set Control Field to **`app_code`**.
3. **Owner Filter**: Add Drop-down list $\rightarrow$ Set Control Field to **`owner`**.
4. **Criticality Filter**: Add Drop-down list $\rightarrow$ Set Control Field to **`criticidade`**.
5. **Date Range Filter**: Click **`Add a control`** $\rightarrow$ **`Date range control`** $\rightarrow$ Place on top-right.

---

## 🔄 Live Data Generation & Auto-Refresh

Run the ADK agent CLI to generate fresh token sessions:

```bash
# 1. Run live agent (Gemini 1.5 Flash)
.venv/bin/python3 src/run_official_adk_agent.py

# 2. Run with Gemini 1.5 Pro or Gemini 2.0 Flash
.venv/bin/python3 src/run_official_adk_agent.py --model=gemini-1.5-pro
.venv/bin/python3 src/run_official_adk_agent.py --model=gemini-2.0-flash

# 3. Seed multi-workload matrix with all 10 Customer Policy Tags
.venv/bin/python3 src/run_official_adk_agent.py --batch
```

👉 In Looker Studio, click the **three dots icon `⋮`** (top-right) $\rightarrow$ **`Refresh data`** (or press `Cmd + Shift + E`). All scorecards, donut charts, cost center breakdowns, and tables will update immediately! 🚀
