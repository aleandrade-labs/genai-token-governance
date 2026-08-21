# 📊 Looker Studio GenAI & ADK Governance: Complete Click-by-Click Guide

**Audience:** FinOps Specialists, Cloud Architects, AI Platform Engineers, Executives  
**Goal:** Build the complete **Executive GenAI Token & Cost Governance Dashboard** in Google Looker Studio in **under 5 minutes** with zero coding.

---

## 🎯 What You Will Build

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🧠 GOOGLE CLOUD FINOPS — GENAI & ADK AGENT GOVERNANCE DASHBOARD                                          │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  [ Filter: SAP Cost Center ▼ ]   [ Filter: App Code ▼ ]   [ Filter: Date Range: Last 30 Days 📅 ]        │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                          │
│  [ Total Sessions ]   [ Total Tokens ]       [ Prompt Tokens ]    [ Output Tokens ]   [ Total AI Cost ]  │
│         8                  41.7 K                 37.6 K               4.1 K               $ 0.02 USD    │
│                                                                                                          │
├────────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│  👤 TOP GENAI CONSUMERS (USER LEADERBOARD)         │  🤖 MODEL FAMILY DISTRIBUTION                       │
│  ┌────────────────────────┬─────────────┬─────────┐│  ┌────────────────────────┬─────────────┬─────────┐ │
│  │ User / Email           │ Tokens      │ Cost $  ││  │ Model Name             │ Tokens      │ Share % │ │
│  ├────────────────────────┼─────────────┼─────────┤│  ├────────────────────────┼─────────────┼─────────┤ │
│  │ admin@altostrat.com    │    28.0 K   │ $ 0.00  ││  │ gemini-1.5-flash       │   25.5 K    │  61.0%  │ │
│  │ alexandrade@google.com │     9.3 K   │ $ 0.01  ││  │ gemini-1.5-pro         │    9.3 K    │  22.3%  │ │
│  │ sa-finops-governance...│     4.4 K   │ $ 0.00  ││  │ gemini-2.0-flash       │    7.0 K    │  16.7%  │ │
│  └────────────────────────┴─────────────┴─────────┘│  └────────────────────────┴─────────────┴─────────┘ │
├────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┤
│  🏢 ERP FINANCIAL CHARGEBACK (SAP COST CENTERS & APP CODES)                                              │
│  ┌─────────────┬─────────────┬───────────────────────────┬──────────────┬──────────────────┐             │
│  │ Cost Center │ App Code    │ Application Name          │ Total Tokens │ Allocated Cost $ │             │
│  ├─────────────┼─────────────┼───────────────────────────┼──────────────┼──────────────────┤             │
│  │ 18207041    │ cds-34242   │ energy_watch_grid         │   15.2 K     │ $ 0.00           │             │
│  │ 12272260    │ cds-59339   │ conexao_silvestre_pd      │    9.3 K     │ $ 0.01           │             │
│  │ 18207115    │ cds-91023   │ substation_copilot        │    7.0 K     │ $ 0.00           │             │
│  │ 18207243    │ cds-34199   │ attendance_sac            │    5.9 K     │ $ 0.00           │             │
│  │ 18206922    │ cds-77211   │ smart_meter_rag           │    4.4 K     │ $ 0.00           │             │
│  ├─────────────┼─────────────┼───────────────────────────┼──────────────┼──────────────────┤             │
│  │ TOTAL       │             │                           │   41.7 K     │ $ 0.02           │             │
│  └─────────────┴─────────────┴───────────────────────────┴──────────────┴──────────────────┘             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ BigQuery Data Source Options

You have **two flexible ways** to connect Looker Studio to BigQuery dataset `genai_finops_governance`:

| Method | Recommended Table / View | Why Choose It? |
| :--- | :--- | :--- |
| **Option A (Recommended)** | `v_genai_governance_dashboard` *(or `agent_events`)* | **Single Unified Data Source**: All top filters (Cost Center, User, App Code, Date Range) cross-filter **every single chart** automatically! |
| **Option B** | Dedicated Views (`v_adk_user_leaderboard`, `v_adk_model_distribution`, etc.) | **Pre-Aggregated Views**: Each chart points to its specialized SQL view. |

---

## 🚀 Step 1: Create Report & Connect to BigQuery (30 seconds)

1. Open your browser and go to **[https://lookerstudio.google.com/](https://lookerstudio.google.com/)**.
2. Click the **`+ Create`** button in the top-left corner $\rightarrow$ click **`Report`**.
3. A popup titled **"Add data to report"** will appear:
   - Click the **`BigQuery`** connector tile.
   - In the columns that appear, select:
     - **Column 1 (Projects)**: Click **`MY PROJECTS`** $\rightarrow$ select **`aleorg-dev-workload-01`**.
     - **Column 2 (Dataset)**: Select **`genai_finops_governance`**.
     - **Column 3 (Table / View)**: Select **`v_genai_governance_dashboard`** *(or `agent_events`)*.
   - Click the blue **`Add`** button in the bottom-right corner.
   - In the confirmation dialog ("You are about to add data to this report"), click **`Add to Report`**.

---

## 🎨 Step 2: Set Report Title & Theme (15 seconds)

1. In the top-left corner, click where it says **"Untitled Report"** and rename to:  
   **`Google Cloud FinOps — GenAI & ADK Governance`**.
2. Look at the default table that appeared on the canvas: click it once and press **`Backspace` / `Delete`** to clear the canvas.
3. In the top toolbar, click **`Theme and layout`** on the right:
   - Choose **Simple Dark** (or keep Simple Light if you prefer white).

---

## 🔢 Step 3: Add Top KPI Scorecards (1 minute)

### Card 1: Grand Total Tokens
1. In the top menu toolbar, click **`Add a chart`** $\rightarrow$ click the **`Scorecard`** icon (`123`).
2. Click near the top-left of the canvas.
3. On the right sidebar (**`SETUP`** tab):
   - **Metric**: Select **`total_tokens`** (Aggregation: `SUM`).
4. Click the **`STYLE`** tab:
   - Check **`Compact numbers`** (formats as `41.7K`).
   - Center-align the number.

### Clone Cards 2, 3, 4, 5 in Seconds:
1. Click Card 1, press **`Cmd+C`**, then **`Cmd+V`** 4 times.
2. Drag them side-by-side across the top row:
   - **Card 2 (Total Sessions)**: Change Metric to **`session_id`** (Aggregation: `COUNT_DISTINCT`).
   - **Card 3 (Prompt Tokens)**: Change Metric to **`prompt_tokens`** (Aggregation: `SUM`).
   - **Card 4 (Output Tokens)**: Change Metric to **`output_tokens`** (Aggregation: `SUM`).
   - **Card 5 (Total AI Cost)**: Change Metric to **`estimated_cost_usd`** (Aggregation: `SUM`, Style: Decimal precision 2).

---

## 👤 Step 4: Add User Leaderboard Table (1 minute)

1. In the top toolbar, click **`Add a chart`** $\rightarrow$ select **`Table`** (or **`Table with heatmap`**).
2. Draw the table on the left side under the scorecards.
3. On the right sidebar (**`SETUP`** tab):
   - **Dimension**: Select **`user_id`**.
   - **Metrics**: Add **`total_tokens`** (SUM) and **`estimated_cost_usd`** (SUM).
   - **Sort**: Select **`total_tokens`** $\rightarrow$ **`Descending`**.
   - *(Optional Filter)*: Add filter `event_type = 'LLM_RESPONSE'`.
4. On the **`STYLE`** tab:
   - Under Metric #1 (`total_tokens`), change Number dropdown to **`Heatmap`** (or Bar).

---

## 🤖 Step 5: Add Model Distribution Donut Chart (1 minute)

1. In the top toolbar, click **`Add a chart`** $\rightarrow$ select **`Donut chart`**.
2. Place the chart on the right side next to the User Leaderboard.
3. On the right sidebar (**`SETUP`** tab):
   - **Dimension**: Select **`model_name`** (e.g. `gemini-1.5-flash`, `gemini-1.5-pro`, `gemini-2.0-flash`).
   - **Metric**: Select **`total_tokens`** (SUM).
   - *(Optional Filter)*: Add filter `event_type = 'LLM_RESPONSE'`.
4. On the **`STYLE`** tab:
   - Set **Hole radius** to **60%**.
   - Set **Slice label** to **Percentage**.

---

## 🏢 Step 6: Add SAP Cost Center Financial Chargeback Table (1 minute)

1. In the top toolbar, click **`Add a chart`** $\rightarrow$ select **`Table`**.
2. Draw the table across the bottom half of the canvas.
3. On the right sidebar (**`SETUP`** tab):
   - **Dimensions**: Add **`cost_center`**, **`app_code`**, **`app_name`**, **`environment`**.
   - **Metrics**: Add **`total_tokens`** (SUM), **`estimated_cost_usd`** (SUM).
   - **Sort**: Select **`total_tokens`** $\rightarrow$ **`Descending`**.
   - *(Optional Filter)*: Add filter `event_type = 'LLM_RESPONSE'`.
4. On the **`STYLE`** tab:
   - Scroll down and check **`Show summary row`** (adds the `TOTAL` row automatically).

---

## ⚡ Step 7: Add Autonomous Tool Analytics Bar Chart (Optional)

1. In the top toolbar, click **`Add a chart`** $\rightarrow$ select **`Bar chart`** (Horizontal).
2. Place it on the canvas.
3. On the right sidebar (**`SETUP`** tab):
   - **Dimension**: Select **`tool_name`** (e.g. `query_substation_status`, `calculate_feeder_loss`).
   - **Metric**: Select **`Record Count`** (or `latency_ms` AVG).
   - **Filter**: Add filter `event_type = 'TOOL_COMPLETED'`.

---

## 🎛️ Step 8: Add Top Dropdown & Date Filters (30 seconds)

1. In the top toolbar, click **`Add a control`** $\rightarrow$ select **`Drop-down list`**.
   - **Control field**: Select **`cost_center`**.
2. Add a second control for **`app_code`** (or `user_id`).
3. Add a third control: click **`Add a control`** $\rightarrow$ select **`Date range control`** $\rightarrow$ place in top-right.

---

## 🔄 Refreshing and Generating Live Data

Whenever you run the agent CLI:

```bash
# 1. Run live agent
.venv/bin/python3 src/run_official_adk_agent.py

# 2. Run with Gemini 1.5 Pro or Gemini 2.0 Flash
.venv/bin/python3 src/run_official_adk_agent.py --model=gemini-1.5-pro
.venv/bin/python3 src/run_official_adk_agent.py --model=gemini-2.0-flash

# 3. Populate multi-workload enterprise matrix
.venv/bin/python3 src/run_official_adk_agent.py --batch
```

👉 In Looker Studio, click the **three dots icon `⋮`** in the top-right $\rightarrow$ click **`Refresh data`** (or press `Cmd + Shift + E`). All charts, scorecards, and tables will update immediately! 🚀
