# 📊 Looker Studio GenAI & ADK Governance: Complete Click-by-Click Guide

**Audience:** FinOps Specialists, Cloud Architects, AI Platform Engineers, C-Level Executives  
**Goal:** Build the complete **Executive GenAI Token, Value Transformation & Label Governance Cockpit** in Google Looker Studio in **under 5 minutes** with zero coding.

---

## 🎯 What You Will Build

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

## 🏷️ Complete Field Dictionary in BigQuery

The BigQuery views (`v_genai_governance_dashboard` and `v_value_transformation_dashboard`) expose all dimensions:

| Field Name | Type | Example Values | Description / Usage |
| :--- | :--- | :--- | :--- |
| **`qualificado_como`** | `STRING` | `Receita`, `Transformacional`, `Corporativo`, `Core` | Strategic Business Category |
| **`valor`** | `STRING` | `Alto`, `Médio`, `Baixo` | Strategic Business Value Tier |
| **`budget_usd`** | `FLOAT64` | `20000.0`, `10000.0`, `40000.0` | Approved Departmental AI Budget |
| **`token_errors`** | `INT64` | `0`, `1`, `2` | Number of token errors encountered |
| **`agent_name`** | `STRING` | `Agent-Vendas`, `Agent-Juridico`, `Agent-RH` | Autonomous Agent Name |
| **`cost_center`** | `STRING` | `18207041`, `18207243`, `18206922` | SAP ERP Financial Cost Center |
| **`app_code`** | `STRING` | `cds-34242`, `cds-77211`, `cds-91023` | Corporate CMDB Application Code |
| **`owner`** | `STRING` | `comercial`, `juridico`, `arquitetura`, `rh` | Squad / Department Owner |
| **`environment`** | `STRING` | `prod`, `hml`, `dev` | Deployment environment tier |
| **`criticidade`** | `STRING` | `sim`, `nao` | Mission-critical system indicator |
| **`it_core`** | `STRING` | `sim`, `nao` | Core enterprise grid infrastructure indicator |
| **`equipe_do_servico`** | `STRING` | `squad_vendas`, `squad_juridico`, `squad_cloud` | Engineering squad |
| **`gerencia_responsavel`**| `STRING`| `gerencia_comercial`, `gerencia_juridica` | Executive leadership department |
| **`business_owner`** | `STRING` | `lucia_mendes`, `evandro_costa`, `raphael_cano`| Corporate business executive |
| **`model_name`** | `STRING` | `gemini-2.5-pro`, `gemini-2.5-flash` | Foundation Model deployed |
| **`tool_name`** | `STRING` | `query_scada_historian`, `sap_erp_billing` | Function call / autonomous tool |

---

## 🗄️ Step 0: Connect BigQuery to Looker Studio

1. Open **[https://lookerstudio.google.com/](https://lookerstudio.google.com/)** $\rightarrow$ Click **`+ Create`** $\rightarrow$ **`Report`**.
2. Select **`BigQuery`** connector:
   - **Project**: `aleorg-dev-workload-01`
   - **Dataset**: `genai_finops_governance`
   - **Table / View**: **`v_genai_governance_dashboard`** *(or `v_value_transformation_dashboard`)*.
3. Click **`Add`** $\rightarrow$ Click **`Add to Report`**.
4. *(If refreshing existing report)*: Go to **Resource > Manage added data sources > Edit** $\rightarrow$ Click **"Refresh fields"** in the bottom-left corner.

---

## 🎛️ Step 1: Top Dropdown Filters

Add dropdown controls across the top row:

1. **Cost Center Filter**:
   - Control Type: **Drop-down list**
   - Control Field: `cost_center`
2. **App Code Filter**:
   - Control Type: **Drop-down list**
   - Control Field: `app_code`
3. **Qualificado Como Filter (NEW)**:
   - Control Type: **Drop-down list**
   - Control Field: **`qualificado_como`**
4. **Valor Estratégico Filter (NEW)**:
   - Control Type: **Drop-down list**
   - Control Field: **`valor`**
5. **Date Range Control**:
   - Default: *Last 30 days* or *Fixed Range*.

---

## 🔢 Step 2: Executive KPI Scorecards

Add 5 scorecards side-by-side:

| Scorecard | Metric Field | Aggregation | Display Name | Format |
| :--- | :--- | :--- | :--- | :--- |
| **Card 1** | `session_id` | `COUNT_DISTINCT` | **`Total Sessions`** | Number (`1.1K`) |
| **Card 2** | `total_tokens` | `SUM` | **`Total Tokens`** | Compact (`30.1M`) |
| **Card 3** | `prompt_tokens` | `SUM` | **`Prompt Tokens`** | Compact (`26.6M`) |
| **Card 4** | `output_tokens` | `SUM` | **`Output Tokens`** | Compact (`3.5M`) |
| **Card 5** | `estimated_cost_usd` | `SUM` | **`Total AI Cost`** | Currency USD (`$22.91`) |

---

## 🍩 Step 3: Donut Charts (Category, Value & Models)

### Chart 1: Business Category (`qualificado_como`)
- **Chart Type:** Donut Chart
- **Dimension:** `qualificado_como`
- **Metric:** `SUM(total_tokens)`
- **Display:** Slices for `Receita`, `Transformacional`, `Corporativo`, `Core`.

### Chart 2: Strategic Value Tier (`valor`)
- **Chart Type:** Donut Chart
- **Dimension:** `valor`
- **Metric:** `SUM(total_tokens)`
- **Display:** Slices for `Alto` vs `Baixo`.

### Chart 3: Foundation Model Distribution
- **Chart Type:** Donut Chart
- **Dimension:** `model_name`
- **Metric:** `SUM(total_tokens)`
- **Display:** Slices for `gemini-2.5-pro`, `gemini-2.5-flash`, etc.

---

## ⚡ Step 4: Fix Autonomous Tool Invocations Chart

To remove the empty/blank top bar in the Tool Invocations chart:

1. Select your existing **Horizontal Bar Chart** for Tools.
2. In the right-hand **Setup** panel:
   - **Dimension:** `tool_name`
   - **Metric:** `Record Count`
3. Scroll down to **Filter** $\rightarrow$ Click **`+ Add a Filter`** $\rightarrow$ **`Create a Filter`**:
   - **Name:** `Exclude Null Tools`
   - **Include/Exclude:** `Include`
   - **Field:** `tool_name`
   - **Condition:** `Is not null`
4. Click **Save**. *The top blank bar immediately vanishes!*

---

## 📋 Step 5: Light AI Value Transformation & Budget Matrix Table

Add a rich table mapping 1-to-1 with the customer's executive spreadsheet:

| Setting | Value / Field |
| :--- | :--- |
| **Chart Type** | **Table with Heatmap / Bars** |
| **Dimension 1** | `agent_name` |
| **Dimension 2** | `user_id` |
| **Dimension 3** | `qualificado_como` |
| **Dimension 4** | `valor` |
| **Metric 1** | `MAX(budget_usd)` *(Formatted as Currency $)* |
| **Metric 2** | `SUM(total_tokens)` *(Formatted with Bar)* |
| **Metric 3** | `SUM(estimated_cost_usd)` *(Formatted as Currency $ with Heatmap)* |
| **Metric 4** | `SUM(token_errors)` *(Formatted as Number)* |
| **Sort** | `SUM(total_tokens)` **Descending** |

---

## 🏢 Step 6: 10 Customer Policy Tags SAP Chargeback Table

At the bottom of the page, add the full 10-tag audit matrix:

| Dimensions | Metrics |
| :--- | :--- |
| `cost_center`, `app_code`, `environment`, `criticidade`, `it_core`, `owner`, `equipe_do_servico`, `gerencia_responsavel`, `business_owner` | `SUM(total_tokens)`, `SUM(estimated_cost_usd)` |

---

## 🚀 How to Populate & Refresh Data in BigQuery

### 1. High-Volume Batch Generator (Simulated Millions of Tokens):
```bash
cd /Users/alexandrade/codes/catlab/light/genai-token-governance
.venv/bin/python3 src/generate_value_transformation_batch.py --sessions 500 --days 30
```

### 2. Live Vertex AI Gemini Real API Batch:
```bash
cd /Users/alexandrade/codes/catlab/light/genai-token-governance
.venv/bin/python3 src/run_live_gemini_batch.py --rounds 2
```
