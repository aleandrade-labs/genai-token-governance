# 📊 Executive Looker Studio Cockpit: Complete Build Guide & Data Architecture

**Audience:** FinOps Specialists, Cloud Architects, AI Platform Engineers, C-Level Executives  
**Goal:** Build the complete **Executive GenAI Token, Value Transformation & Label Governance Cockpit** in Google Looker Studio in **under 5 minutes** with zero coding.

---

## 🧠 Executive Vision: What We Are Collecting & Why

The engine streams **100% genuine real-time telemetry** from Google Vertex AI and the Google Agent Development Kit (ADK) into BigQuery across **3 foundational governance planes**:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               3 PILLARS OF ENTERPRISE GENAI GOVERNANCE                          │
├───────────────────────────────┬──────────────────────────────────┬───────────────────────────────┤
│  🏢 1. FINANCIAL CHARGEBACK   │  🎯 2. STRATEGIC VALUE PLANE     │  ⚡ 3. OPERATIONAL METRICS    │
│  (SAP ERP / CMDB Policy Tags) │  (Business Value Transformation) │  (Vertex AI Real Telemetry)   │
├───────────────────────────────┼──────────────────────────────────┼───────────────────────────────┤
│ • cost_center (SAP ERP)       │ • qualificado_como (Receita,     │ • prompt_tokens (Vertex AI)   │
│ • app_code (CMDB Code)        │   Transformacional, Core...)     │ • output_tokens (Candidates)  │
│ • owner (Squad/Department)    │ • valor (Alto vs Baixo)          │ • total_tokens (Live Count)   │
│ • environment (prod/hml/dev)  │ • budget_usd (Dept Budget)       │ • latency_ms (Real Roundtrip) │
│ • criticidade (sim/nao)       │ • token_errors (Failure Rates)   │ • estimated_cost_usd ($/1M)   │
│ • it_core (sim/nao)           │ • business_owner (Executive)     │ • tool_name (Function Calls)  │
│ • equipe_do_servico (Squad)   │ • gerencia_responsavel (Dept)    │ • model_name (Pro/Flash/Lite) │
└───────────────────────────────┴──────────────────────────────────┴───────────────────────────────┘
```

---

## 🎯 What You Will Build (Exact Dashboard Layout)

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🧠 GOOGLE CLOUD FINOPS — GENAI TOKEN GOVERNANCE & AI VALUE TRANSFORMATION COCKPIT                                     │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  [ Cost Center ▼ ]  [ App Code ▼ ]  [ Qualificado Como ▼ ]  [ Valor ▼ ]  [ Agent Name ▼ ]  [ Date: Aug 1 - Sep 2 📅 ]   │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                        │
│  [ Total Sessions ]     [ Total Tokens ]      [ Prompt Tokens ]     [ Output Tokens ]     [ Total AI Cost (USD) ]      │
│        1.1 K                 30.1 M                26.6 M                3.5 M                   $ 22.91               │
│                                                                                                                        │
├────────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────────┤
│  👤 TOP GENAI CONSUMERS (USER LEADERBOARD)             │  🍩 BUSINESS CATEGORY (`qualificado_como`)                    │
│  ┌────────────────────────────┬─────────────┬─────────┐│  ┌────────────────────────────┬─────────────┬───────────────┐ │
│  │ User / Email               │ Tokens      │ Cost $  ││  │ Categoria                  │ Tokens      │ Share %       │ │
│  ├────────────────────────────┼─────────────┼─────────┤│  ├────────────────────────────┼─────────────┼───────────────┤ │
│  │ lucia@light.com.br         │    3.15 M   │ $ 0.37  ││  │ Core                       │   21.7 M    │  72.1%        │ │
│  │ evandro@light.com.br       │    2.80 M   │ $ 4.13  ││  │ Corporativo                │    4.4 M    │  14.7%        │ │
│  │ senna@light.com.br         │    2.47 M   │ $ 3.75  ││  │ Receita                    │    3.1 M    │  10.5%        │ │
│  │ jesus@light.com.br         │    2.18 M   │ $ 0.07  ││  │ Transformacional           │    2.8 M    │   9.3%        │ │
│  └────────────────────────────┴─────────────┴─────────┘│  └────────────────────────────┴─────────────┴───────────────┘ │
├────────────────────────────────────────────────────────┼───────────────────────────────────────────────────────────────┤
│  🤖 AUTONOMOUS AGENT LEADERBOARD                       │  ⚡ AUTONOMOUS TOOL INVOCATIONS (Filtered)                     │
│  ┌────────────────────────────┬─────────────┬─────────┐│  ┌────────────────────────────┬─────────────┬───────────────┐ │
│  │ Agent Name                 │ Tokens      │ Cost $  ││  │ Tool Name                  │ Calls       │ Status        │ │
│  ├────────────────────────────┼─────────────┼─────────┤│  ├────────────────────────────┼─────────────┼───────────────┤ │
│  │ Agent-Vendas               │    3.15 M   │ $ 0.62  ││  │ query_scada_historian      │     217     │ 100% OK       │ │
│  │ Agent-Juridico             │    2.80 M   │ $ 4.52  ││  │ hr_payroll_database        │     125     │ 100% OK       │ │
│  │ Agent-IT                   │    2.47 M   │ $ 4.11  ││  │ customer_satisfaction_score│     121     │ 100% OK       │ │
│  │ Agent-Operacao             │    2.18 M   │ $ 0.31  ││  │ sap_erp_billing_lookup     │     120     │ 100% OK       │ │
│  │ Executive-Agent            │    1.60 M   │ $ 2.65  ││  │ substation_telemetry_fetch │     118     │ 100% OK       │ │
│  └────────────────────────────┴─────────────┴─────────┘│  └────────────────────────────┴─────────────┴───────────────┘ │
├────────────────────────────────────────────────────────┴───────────────────────────────────────────────────────────────┤
│  📋 LIGHT AI VALUE TRANSFORMATION & BUDGET GOVERNANCE TABLE                                                            │
│  ┌──────────────────┬──────────────────────┬──────────────────┬───────┬────────────┬─────────────┬───────────┬───────┐ │
│  │ Agent Name       │ User                 │ Qualificado Como │ Valor │ Budget ($) │ Tokens      │ Cost ($)  │ Error │ │
│  ├──────────────────┼──────────────────────┼──────────────────┼───────┼────────────┼─────────────┼───────────┼───────┤ │
│  │ Agent-Vendas     │ lucia@light.com.br   │ Receita          │ Alto  │ $ 20,000   │  3,153,565  │ $ 0.62    │   0   │ │
│  │ Agent-Juridico   │ evandro@light.com.br │ Transformacional │ Alto  │ $ 10,000   │  2,806,956  │ $ 4.52    │   0   │ │
│  │ Agent-IT         │ senna@light.com.br   │ Corporativo      │ Alto  │ $ 10,000   │  2,476,118  │ $ 4.11    │   0   │ │
│  │ Agent-Operacao   │ jesus@light.com.br   │ Core             │ Baixo │ $ 10,000   │  2,181,544  │ $ 0.31    │   0   │ │
│  │ Executive-Agent  │ jorge_sanchez@...    │ Core             │ Alto  │ $  2,020   │  1,604,217  │ $ 2.65    │   0   │ │
│  │ AI-Agentic       │ juan@light.com.br    │ Core             │ Alto  │ $  2,026   │  1,588,050  │ $ 2.59    │   0   │ │
│  │ AI-Gov           │ omar@light.com.br    │ Core             │ Alto  │ $  2,023   │  1,285,614  │ $ 0.61    │   0   │ │
│  │ Agent-RH         │ victor@light.com.br  │ Corporativo      │ Alto  │ $ 40,000   │  1,256,330  │ $ 0.13    │   0   │ │
│  └──────────────────┴──────────────────────┴──────────────────┴───────┴────────────┴─────────────┴───────────┴───────┘ │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  🏢 COMPLETE ENTERPRISE FINANCIAL CHARGEBACK (ALL 10 CUSTOMER POLICY TAGS)                                             │
│  ┌──────────┬───────────┬──────────────┬──────────┬─────────┬───────────┬──────────────────────┬─────────────┬─────────┐ │
│  │ Cost Ctr │ App Code  │ Environment  │ Critical │ IT Core │ Owner     │ Gerência Responsável │ Tokens      │ Cost ($)│ │
│  ├──────────┼───────────┼──────────────┼──────────┼─────────┼───────────┼──────────────────────┼─────────────┼─────────┤ │
│  │ 18207041 │ cds-34242 │ prod         │ sim      │ nao     │ comercial │ gerencia_comercial   │ 3,153,565   │ $ 0.37  │ │
│  │ 18206922 │ cds-77211 │ prod         │ sim      │ nao     │ juridico  │ gerencia_juridica    │ 2,806,956   │ $ 4.13  │ │
│  │ 18207115 │ cds-91023 │ prod         │ sim      │ sim     │ arquit.   │ gerencia_de_sistemas │ 2,476,118   │ $ 3.75  │ │
│  └──────────┴───────────┴──────────────┴──────────┴─────────┴───────────┴──────────────────────┴─────────────┴─────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🏷️ BigQuery Data Dictionary (`v_genai_governance_dashboard`)

The BigQuery unified view exposes all fields ready for instant drag-and-drop analytics:

| Category | Field Name | Type | Example Values | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Value Plane** | **`qualificado_como`** | `STRING` | `Receita`, `Transformacional`, `Corporativo`, `Core` | Strategic Business Category |
| **Value Plane** | **`valor`** | `STRING` | `Alto`, `Médio`, `Baixo` | Strategic Business Value Tier |
| **Value Plane** | **`budget_usd`** | `FLOAT64` | `20000.0`, `10000.0`, `40000.0` | Approved Departmental AI Budget |
| **Value Plane** | **`token_errors`** | `INT64` | `0`, `1`, `2` | Number of token / tool errors |
| **Identity** | **`agent_name`** | `STRING` | `Agent-Vendas`, `Agent-Juridico`, `Agent-RH` | Specialized AI Agent Name |
| **Identity** | **`user_id`** | `STRING` | `lucia@light.com.br`, `evandro@light.com.br` | User email initiating the call |
| **SAP FinOps** | **`cost_center`** | `STRING` | `18207041`, `18207243`, `18206922` | SAP ERP Cost Center for Chargeback |
| **SAP FinOps** | **`app_code`** | `STRING` | `cds-34242`, `cds-77211`, `cds-91023` | Corporate CMDB Application Code |
| **SAP FinOps** | **`owner`** | `STRING` | `comercial`, `juridico`, `arquitetura`, `rh` | Squad / Department Owner |
| **SAP FinOps** | **`environment`** | `STRING` | `prod`, `hml`, `dev` | Deployment environment tier |
| **SAP FinOps** | **`criticidade`** | `STRING` | `sim`, `nao` | Mission-critical system indicator |
| **SAP FinOps** | **`it_core`** | `STRING` | `sim`, `nao` | Core enterprise grid infrastructure |
| **SAP FinOps** | **`equipe_do_servico`** | `STRING` | `squad_vendas`, `squad_juridico`, `squad_cloud` | Engineering squad |
| **SAP FinOps** | **`gerencia_responsavel`**| `STRING`| `gerencia_comercial`, `gerencia_juridica` | Executive leadership department |
| **SAP FinOps** | **`business_owner`** | `STRING` | `lucia_mendes`, `evandro_costa`, `raphael_cano`| Corporate business executive |
| **GenAI Ops** | **`model_name`** | `STRING` | `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite` | Vertex AI Foundation Model |
| **GenAI Ops** | **`tool_name`** | `STRING` | `query_scada_historian`, `sap_erp_billing` | Function call / autonomous tool |
| **GenAI Ops** | **`prompt_tokens`** | `INT64` | `41`, `1250`, `3420` | Real Input Tokens (Vertex AI) |
| **GenAI Ops** | **`output_tokens`** | `INT64` | `2935`, `3553`, `4128` | Real Candidate Tokens (Vertex AI) |
| **GenAI Ops** | **`total_tokens`** | `INT64` | `4523`, `5161`, `8231` | Total Tokens Emitted |
| **GenAI Ops** | **`latency_ms`** | `FLOAT64` | `12879.0`, `30643.0`, `47342.0` | Real Execution Latency (ms) |
| **GenAI Ops** | **`estimated_cost_usd`**| `FLOAT64`| `$0.000884`, `$0.012969` | Real Cost calculated from Pricing |

---

## 🛠️ Step-by-Step Construction Guide (Under 5 Minutes)

### Step 0: Connect BigQuery to Looker Studio
1. Open **[https://lookerstudio.google.com/](https://lookerstudio.google.com/)** $\rightarrow$ Click **`+ Create`** $\rightarrow$ **`Report`**.
2. Select **`BigQuery`** connector:
   - **Project**: `aleorg-dev-workload-01`
   - **Dataset**: `genai_finops_governance`
   - **Table / View**: **`v_genai_governance_dashboard`**
3. Click **`Add`** $\rightarrow$ Click **`Add to Report`**.
4. *(If refreshing existing report)*: Go to **Resource > Manage added data sources > Edit** $\rightarrow$ Click **"Refresh fields"** in the bottom-left corner.

---

### Step 1: Top Dropdown Controls (Filters)
Add 5 controls side-by-side along the top bar (`Insert > Drop-down list`):

1. **Cost Center Filter**:
   - Control Field: `cost_center`
2. **App Code Filter**:
   - Control Field: `app_code`
3. **Qualificado Como Filter (NEW)**:
   - Control Field: **`qualificado_como`**
4. **Valor Estratégico Filter (NEW)**:
   - Control Field: **`valor`**
5. **Agent Name Filter (NEW)**:
   - Control Field: **`agent_name`**
6. **Date Range Control**:
   - `Insert > Date range control` $\rightarrow$ Set Default to *Auto / Last 30 Days*.

---

### Step 2: Top KPI Scorecards
Add 5 scorecards side-by-side (`Insert > Scorecard`):

| Card # | Metric Field | Aggregation | Display Name | Format / Style |
| :--- | :--- | :--- | :--- | :--- |
| **Card 1** | `session_id` | `COUNT_DISTINCT` | **`Total Sessions`** | Decimal: `0` (e.g. `1.1K`) |
| **Card 2** | `total_tokens` | `SUM` | **`Total Tokens`** | Compact Numbers (e.g. `30.1M`) |
| **Card 3** | `prompt_tokens` | `SUM` | **`Prompt Tokens`** | Compact Numbers (e.g. `26.6M`) |
| **Card 4** | `output_tokens` | `SUM` | **`Output Tokens`** | Compact Numbers (e.g. `3.5M`) |
| **Card 5** | `estimated_cost_usd` | `SUM` | **`Total AI Cost`** | Currency: `USD ($)` (e.g. `$22.91`) |

---

### Step 3: Top Consumers Leaderboard (User Table)
Add a Table on the middle-left (`Insert > Table`):

- **Dimension:** `user_id`
- **Metric 1:** `SUM(total_tokens)`
  - *Style Tab:* Show as **Bar / Data Bar** (Blue)
- **Metric 2:** `SUM(estimated_cost_usd)`
  - *Style Tab:* Show as **Heatmap** (Orange)
- **Sort:** `SUM(total_tokens)` Descending
- **Rows Per Page:** `10`

---

### Step 4: Business Category Donut Chart (`qualificado_como`)
Add a Donut Chart on the middle-right (`Insert > Pie chart > Donut`):

- **Dimension:** `qualificado_como`
- **Metric:** `SUM(total_tokens)`
- **Slices displayed:** `Receita`, `Transformacional`, `Corporativo`, `Core`
- *Insight:* Shows C-level leadership the exact % of token investments powering Revenue Growth vs. Core Operations.

---

### Step 5: Autonomous Agent Leaderboard Table
Add a Table on the lower-left (`Insert > Table`):

- **Dimension:** `agent_name`
- **Metric 1:** `SUM(total_tokens)` (Formatted with Bar)
- **Metric 2:** `SUM(estimated_cost_usd)` (Formatted as Currency `$`)
- **Metric 3:** `AVG(latency_ms)` (Formatted as Number `ms`)
- **Sort:** `SUM(total_tokens)` Descending

---

### Step 6: Autonomous Tool Invocations Chart (Filtered & Cleaned)
Add a Horizontal Bar Chart on the lower-right (`Insert > Bar chart > Horizontal`):

- **Dimension:** `tool_name`
- **Metric:** `Record Count`
- **Filter (Crucial Step):**
  1. In the right-hand **Setup** panel, scroll down to **Filter** $\rightarrow$ Click **`+ Add a Filter`** $\rightarrow$ **`Create a Filter`**.
  2. **Name:** `Exclude Null Tools`
  3. **Clause:** `Include` $\rightarrow$ Field: `tool_name` $\rightarrow$ Condition: `Is not null`.
  4. Click **Save**. *The top empty bar disappears and only real function calls (`query_scada`, `sap_erp`, `legal_contract`) are shown!*

---

### Step 7: Light AI Value Transformation & Budget Matrix Table
Add a Full-Width Master Table across the screen (`Insert > Table`):

| Setting | Value / Field |
| :--- | :--- |
| **Dimension 1** | `agent_name` |
| **Dimension 2** | `user_id` |
| **Dimension 3** | `qualificado_como` |
| **Dimension 4** | `valor` |
| **Metric 1** | `MAX(budget_usd)` *(Format: Currency `$`, Precision: `0`)* |
| **Metric 2** | `SUM(total_tokens)` *(Format: Number with Bar)* |
| **Metric 3** | `SUM(estimated_cost_usd)` *(Format: Currency `$`, Heatmap)* |
| **Metric 4** | `SUM(token_errors)` *(Format: Number)* |
| **Sort** | `SUM(total_tokens)` **Descending** |

---

### Step 8: 10 Customer Policy Tags SAP Chargeback Matrix
Add a Bottom Audit Table (`Insert > Table`):

- **Dimensions:** `cost_center`, `app_code`, `environment`, `criticidade`, `it_core`, `owner`, `equipe_do_servico`, `gerencia_responsavel`, `business_owner`
- **Metrics:** `SUM(total_tokens)`, `SUM(estimated_cost_usd)`
- **Sort:** `SUM(total_tokens)` Descending

---

## ⚡ How to Populate with 100% Real Live Tokens

To stream fresh real live tokens from Vertex AI into your dashboard:

```bash
cd /Users/alexandrade/codes/catlab/light/genai-token-governance

# 1. Run 1 live round across all 11 enterprise agents with balanced model tiering:
.venv/bin/python3 src/run_live_gemini_batch.py

# 2. Run 3 live rounds with rotating model distribution (Pro, Flash, Flash-Lite):
.venv/bin/python3 src/run_live_gemini_batch.py --rounds 3 --distribute-models

# 3. In Looker Studio, press Cmd+Shift+R / Ctrl+Shift+R to refresh data!
```
