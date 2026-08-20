# 📊 Looker Studio GenAI & ADK Governance Dashboard Guide

**Audience:** FinOps Analysts, BI Developers, Enterprise Architects, Executives  
**Purpose:** Click-by-click instructions to build the **Executive AI & GenAI Token Governance Dashboard** in Google Looker Studio, connected directly to Google ADK BigQuery Analytics.

---

## 📋 Table of Contents
1. [Executive Dashboard Mockup & Structure](#-1-executive-dashboard-mockup--structure)
2. [BigQuery Views Data Sources Reference](#-2-bigquery-views-data-sources-reference)
3. [Step-by-Step Widget Recipes](#-3-step-by-step-widget-recipes)
4. [Interactive Filtering & Controls](#-4-interactive-filtering--controls)
5. [Automated PDF Export & Stakeholder Scheduling](#-5-automated-pdf-export--stakeholder-scheduling)

---

## 🎨 1. Executive Dashboard Mockup & Structure

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🧠 LIGHT S/A — ADK GENAI & TOKEN GOVERNANCE DASHBOARD                                                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                          │
│  [ Active Sessions ]   [ Total Tokens ]       [ Cache Hit Rate ]   [ Tool Success % ]   [ Total AI Cost ] │
│        1,420                148.2 M                 34.2 %               98.5 %           $ 248.50 USD   │
│                                                                                                          │
├────────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│  👤 TOP GENAI CONSUMERS (USER LEADERBOARD)         │  🤖 MODEL FAMILY VOLUME & COST DISTRIBUTION         │
│  ┌────────────────────────┬─────────────┬─────────┐│  ┌────────────────────────┬─────────────┬─────────┐ │
│  │ User / Email           │ Tokens (M)  │ Cost $  ││  │ Model Name             │ Tokens (M)  │ Share % │ │
│  ├────────────────────────┼─────────────┼─────────┤│  ├────────────────────────┼─────────────┼─────────┤ │
│  │ raphael_cano           │  42.1 M     │ $ 72.50 ││  │ gemini-1.5-flash       │ 104.2 M     │  70.3%  │ │
│  │ antonio_lameirao       │  28.4 M     │ $ 48.20 ││  │ gemini-1.5-pro         │  32.1 M     │  21.7%  │ │
│  │ mariana_souza          │  22.8 M     │ $ 38.10 ││  │ gemini-2.0-flash       │   8.4 M     │   5.7%  │ │
│  │ carlos_eduardo         │  18.7 M     │ $ 31.10 ││  │ text-embedding-004     │   3.5 M     │   2.3%  │ │
│  └────────────────────────┴─────────────┴─────────┘│  └────────────────────────┴─────────────┴─────────┘ │
├────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┤
│  🏢 ERP FINANCIAL CHARGEBACK (SAP COST CENTERS & APP CODES)                                              │
│  ┌─────────────┬─────────────┬───────────────────────────┬──────────────┬──────────────────┐             │
│  │ Cost Center │ App Code    │ Application Name          │ Total Tokens │ Allocated Cost $ │             │
│  ├─────────────┼─────────────┼───────────────────────────┼──────────────┼──────────────────┤             │
│  │ 18207243    │ cds-34199   │ attendance_sac            │  58.4 M      │ $ 98.40          │             │
│  │ 18207041    │ cds-34242   │ energy_watch_grid         │  38.2 M      │ $ 64.10          │             │
│  │ 12272260    │ cds-59339   │ conexao_silvestre_pd      │  31.5 M      │ $ 52.80          │             │
│  │ 18206922    │ cds-77211   │ smart_meter_rag           │  20.1 M      │ $ 33.20          │             │
│  │ 18207115    │ cds-91023   │ substation_copilot        │  14.3 M      │ $ 23.40          │             │
│  └─────────────┴─────────────┴───────────────────────────┴──────────────┴──────────────────┘             │
├────────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│  🛠️ ADK TOOL EXECUTION & PERFORMANCE HEALTH        │  📈 DAILY TOKEN CONSUMPTION & COST TREND            │
│  ┌────────────────────────┬─────────────┬─────────┐│  [ Time Series Chart: Daily Tokens vs Daily Cost $ ] │
│  │ Tool Name              │ Invocations │ Latency ││  • Flash Growth                                    │
│  ├────────────────────────┼─────────────┼─────────┤│  • Pro Optimization                                │
│  │ query_substation_tele  │    1,240    │ 420 ms  ││  • Spend stabilization                             │
│  │ search_technical_rag   │      890    │ 680 ms  ││                                                    │
│  │ calculate_overload     │      410    │ 110 ms  ││                                                    │
│  └────────────────────────┴─────────────┴─────────┘│                                                    │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ 2. BigQuery Views Data Sources Reference

Connect Looker Studio using the native **BigQuery Connector** (`aleorg-dev-workload-01` $\rightarrow$ `genai_finops_governance`):

| View Name | Primary Fields | Best Visual Types |
| :--- | :--- | :--- |
| `v_adk_executive_kpis` | `grand_total_tokens`, `total_prompt_tokens`, `total_output_tokens`, `total_estimated_cost_usd`, `tool_success_rate_pct` | Scorecards |
| `v_adk_user_leaderboard` | `user_id`, `app_code`, `prompt_tokens`, `output_tokens`, `total_tokens`, `estimated_cost_usd` | Table with Heatmap Bars |
| `v_adk_model_distribution` | `model_name`, `total_tokens`, `total_cost_usd`, `avg_latency_ms` | Donut Chart & Bar Chart |
| `v_adk_cost_center_attribution` | `cost_center`, `app_code`, `app_name`, `total_tokens`, `allocated_cost_usd` | Multi-dimension Table |
| `v_adk_tool_analytics` | `tool_name`, `total_invocations`, `success_rate_pct`, `avg_latency_ms` | Table & Horizontal Bar Chart |
| `v_adk_daily_trend` | `usage_date`, `daily_sessions`, `daily_tokens`, `daily_cost_usd` | Time Series Chart |

---

## 🛠️ 3. Step-by-Step Widget Recipes

### 1️⃣ Executive Scorecards (Top Row)
- **Data Source**: `v_adk_executive_kpis`
- **Total Tokens**: Metric: `SUM(grand_total_tokens)`, Number format: Compact (e.g. `148.2 M`).
- **Prompt Tokens**: Metric: `SUM(total_prompt_tokens)`, Number format: Compact.
- **Output Tokens**: Metric: `SUM(total_output_tokens)`, Number format: Compact.
- **Total AI Spend**: Metric: `SUM(total_estimated_cost_usd)`, Number format: USD `$`.
- **Tool Success Rate**: Metric: `AVG(tool_success_rate_pct)`, Number format: Percent `98.5%`.

---

### 2️⃣ User Token Leaderboard (Top Left)
- **Data Source**: `v_adk_user_leaderboard`
- **Chart Type**: Table
- **Dimensions**: `user_id`, `app_name`
- **Metrics**: `SUM(total_tokens)`, `SUM(estimated_cost_usd)`
- **Sorting**: `SUM(total_tokens)` Descending
- **Style**: Enable Heatmap bars on `SUM(total_tokens)`.

---

### 3️⃣ Model Distribution Donut Chart (Top Right)
- **Data Source**: `v_adk_model_distribution`
- **Chart Type**: Donut Chart
- **Dimension**: `model_name`
- **Metric**: `SUM(total_tokens)`
- **Style**: Hole Radius `60%`, Data Labels `Percentage`.

---

### 4️⃣ SAP Cost Center Financial Chargeback Table (Middle)
- **Data Source**: `v_adk_cost_center_attribution`
- **Chart Type**: Table with Summary Row
- **Dimensions**: `cost_center` (SAP), `app_code`, `app_name`, `environment`
- **Metrics**: `SUM(total_tokens)`, `SUM(allocated_cost_usd)`
- **Sorting**: `SUM(allocated_cost_usd)` Descending
- **Style**: Enable "Show summary row", Wrap text.

---

### 5️⃣ ADK Tool Execution & Health (Bottom Left)
- **Data Source**: `v_adk_tool_analytics`
- **Chart Type**: Table
- **Dimension**: `tool_name`
- **Metrics**: `SUM(total_invocations)`, `AVG(success_rate_pct)`, `AVG(avg_latency_ms)`
- **Style**: Decimals for latency set to 0 (e.g. `420 ms`).

---

### 6️⃣ Historical Daily Trend (Bottom Right)
- **Data Source**: `v_adk_daily_trend`
- **Chart Type**: Time Series Chart
- **Dimension**: `usage_date`
- **Metrics**: `SUM(daily_tokens)` (Left Y-Axis), `SUM(daily_cost_usd)` (Right Y-Axis).

---

## 🔍 4. Interactive Filtering & Controls

Place the following Drop-down controls at the top of the report:
1. **SAP Cost Center Selector**: Control Field: `cost_center`.
2. **Application Code Selector**: Control Field: `app_code`.
3. **Model Family Selector**: Control Field: `model_name`.
4. **Date Range Picker**: Default range: **Last 30 Days**.

---

## 📬 5. Automated PDF Export & Stakeholder Scheduling

1. In Looker Studio, click **Share $\rightarrow$ Schedule delivery**.
2. **Recipients**: Add executive stakeholders (`antonio.lameirao@light.com.br`, `raphael.cano@light.com.br`, FinOps leads).
3. **Repeat**: Every Monday at 08:00 AM.
4. **Format**: Attached PDF snapshot with direct report link.
