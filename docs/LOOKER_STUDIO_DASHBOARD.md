# 📊 Looker Studio GenAI & ADK Governance: Complete Click-by-Click Guide

**Audience:** Beginners, FinOps Analysts, Cloud Architects, Executives  
**Goal:** Build the complete **Executive GenAI Token & Cost Governance Dashboard** in Google Looker Studio from scratch in **under 5 minutes** with zero coding.

---

## 🎯 What You Will Build

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  🧠 LIGHT S/A — ADK GENAI & TOKEN GOVERNANCE DASHBOARD                                                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  [ Filter: SAP Cost Center ▼ ]   [ Filter: App Code ▼ ]   [ Filter: Date Range: Last 30 Days 📅 ]        │
├──────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                          │
│  [ Total Sessions ]   [ Total Tokens ]       [ Prompt Tokens ]    [ Output Tokens ]   [ Total AI Cost ]  │
│        200                 1.58 M                 1.31 M               267.4 K             $ 0.41 USD    │
│                                                                                                          │
├────────────────────────────────────────────────────┬─────────────────────────────────────────────────────┤
│  👤 TOP GENAI CONSUMERS (USER LEADERBOARD)         │  🤖 MODEL FAMILY DISTRIBUTION                       │
│  ┌────────────────────────┬─────────────┬─────────┐│  ┌────────────────────────┬─────────────┬─────────┐ │
│  │ User / Email           │ Tokens      │ Cost $  ││  │ Model Name             │ Tokens      │ Share % │ │
│  ├────────────────────────┼─────────────┼─────────┤│  ├────────────────────────┼─────────────┼─────────┤ │
│  │ mariana_souza@light... │   383.4 K   │ $ 0.05  ││  │ gemini-1.5-flash       │  1.10 M     │  70.1%  │ │
│  │ antonio_lameirao@li... │   279.2 K   │ $ 0.06  ││  │ gemini-1.5-pro         │  340.2 K    │  21.5%  │ │
│  │ equipe_transformacao...│   262.5 K   │ $ 0.09  ││  │ gemini-2.0-flash       │   90.1 K    │   5.7%  │ │
│  │ raphael_cano@light...  │   193.5 K   │ $ 0.09  ││  │ text-embedding-004     │   45.6 K    │   2.7%  │ │
│  └────────────────────────┴─────────────┴─────────┘│  └────────────────────────┴─────────────┴─────────┘ │
├────────────────────────────────────────────────────┴─────────────────────────────────────────────────────┤
│  🏢 ERP FINANCIAL CHARGEBACK (SAP COST CENTERS & APP CODES)                                              │
│  ┌─────────────┬─────────────┬───────────────────────────┬──────────────┬──────────────────┐             │
│  │ Cost Center │ App Code    │ Application Name          │ Total Tokens │ Allocated Cost $ │             │
│  ├─────────────┼─────────────┼───────────────────────────┼──────────────┼──────────────────┤             │
│  │ 18207243    │ cds-34199   │ attendance_sac            │  449.6 K     │ $ 0.18           │             │
│  │ 12272260    │ cds-59339   │ conexao_silvestre_pd      │  383.4 K     │ $ 0.05           │             │
│  │ 18207041    │ cds-34242   │ energy_watch_grid         │  279.2 K     │ $ 0.06           │             │
│  │ 18207115    │ cds-91023   │ substation_copilot        │  262.5 K     │ $ 0.09           │             │
│  │ 18206922    │ cds-77211   │ smart_meter_rag           │  204.7 K     │ $ 0.03           │             │
│  ├─────────────┼─────────────┼───────────────────────────┼──────────────┼──────────────────┤             │
│  │ TOTAL       │             │                           │    1.58 M    │ $ 0.41           │             │
│  └─────────────┴─────────────┴───────────────────────────┴──────────────┴──────────────────┘             │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Step 1: Create Report & Connect to BigQuery (30 seconds)

1. Open your browser and go to **[https://lookerstudio.google.com/](https://lookerstudio.google.com/)**.
2. Click the **`+ Create`** button in the top-left corner $\rightarrow$ click **`Report`**.
3. A popup titled **"Add data to report"** will appear:
   - Click the **`BigQuery`** connector tile.
   - In the columns that appear, select:
     - **Column 1 (Projects)**: Click **`MY PROJECTS`** $\rightarrow$ select **`aleorg-dev-workload-01`**.
     - **Column 2 (Dataset)**: Select **`genai_finops_governance`**.
     - **Column 3 (Table)**: Select **`v_adk_user_leaderboard`**.
   - Click the blue **`Add`** button in the bottom-right corner.
   - In the confirmation dialog ("You are about to add data to this report"), click **`Add to Report`**.

---

## 🎨 Step 2: Set Report Title & Theme (15 seconds)

1. In the top-left corner, click where it says **"Untitled Report"** and type:  
   **`Light S/A - GenAI Token & Cost Governance`**.
2. Look at the default table that appeared in the middle of the screen: click it once and press **`Backspace` / `Delete`** on your keyboard to clear the canvas.
3. In the top toolbar, click **`Theme and layout`** (on the right side of the toolbar):
   - Choose the **Simple Dark** or **Edge** theme (or keep Simple Light if you prefer white background).

---

## 🔢 Step 3: Add Top KPI Scorecards (1 minute)

### Card 1: Total Tokens
1. In the top menu toolbar, click **`Add a chart`** $\rightarrow$ click the **`Scorecard`** icon (the box with `123`).
2. Click near the top-left of the blank canvas to place the card.
3. On the right sidebar, ensure you are on the **`SETUP`** tab:
   - Under **Metric**, click the field and select **`total_tokens`**.
4. Click the **`STYLE`** tab on the right sidebar:
   - Check the box for **`Compact numbers`** (this changes `1,579,434` into `1.6M`).
   - Center-align the text.

### Cards 2, 3, 4: Clone in 5 seconds!
1. Click Card 1, press **`Cmd+C`** (or `Ctrl+C`), then press **`Cmd+V`** (or `Ctrl+V`) 3 times to make 3 copies.
2. Drag them side-by-side across the top row.
3. Update their metrics on the **`SETUP`** tab:
   - **Card 2**: Change Metric to **`prompt_tokens`**.
   - **Card 3**: Change Metric to **`output_tokens`**.
   - **Card 4**: Change Metric to **`estimated_cost_usd`** *(In Style tab, set Decimal precision to 2)*.

---

## 👤 Step 4: Add User Leaderboard Table (1 minute)

1. In the top toolbar, click **`Add a chart`** $\rightarrow$ select **`Table`** (or **`Table with heatmap`**).
2. Click on the left side of the canvas below the scorecards to draw the table.
3. On the right sidebar (**`SETUP`** tab):
   - **Dimension**: Drag or select **`user_id`**. *(You can also add `app_code` as a second dimension)*.
   - **Metric**: Drag or select **`total_tokens`** and **`estimated_cost_usd`**.
   - **Sort**: Click the Sort field $\rightarrow$ select **`total_tokens`** $\rightarrow$ choose **`Descending`**.
4. On the right sidebar (**`STYLE`** tab):
   - Check **`Wrap text`** on table body.
   - Under Metric #1 (`total_tokens`), change *Number* dropdown to **`Heatmap`** (or Bar chart).

---

## 🤖 Step 5: Add Model Distribution Donut Chart (1 minute)

1. In the top toolbar, click **`Add a chart`** $\rightarrow$ select **`Donut chart`** (circle with a hole in the middle).
2. Click on the right side of the canvas (next to the User Leaderboard table).
3. On the right sidebar (**`SETUP`** tab):
   - At the very top under **Data Source**, click the existing data source name $\rightarrow$ click **`+ Add Data`** (bottom of list).
   - Select **`BigQuery`** $\rightarrow$ `aleorg-dev-workload-01` $\rightarrow$ `genai_finops_governance` $\rightarrow$ **`v_adk_model_distribution`** $\rightarrow$ click **`Add`**.
   - **Dimension**: Select **`model_name`**.
   - **Metric**: Select **`total_tokens`**.
4. On the right sidebar (**`STYLE`** tab):
   - Set **Hole radius** slider to **60%**.
   - Set **Slice label** to **Percentage**.

---

## 🏢 Step 6: Add SAP Cost Center Financial Chargeback Table (1 minute)

1. In the top toolbar, click **`Add a chart`** $\rightarrow$ select **`Table`**.
2. Click across the bottom half of the canvas to place the table.
3. On the right sidebar (**`SETUP`** tab):
   - Under **Data Source**, click data source $\rightarrow$ click **`+ Add Data`** $\rightarrow$ select **`v_adk_cost_center_attribution`** $\rightarrow$ click **`Add`**.
   - **Dimensions**: Add **`cost_center`**, **`app_code`**, **`app_name`**, **`environment`**.
   - **Metrics**: Add **`total_tokens`**, **`allocated_cost_usd`**.
   - **Sort**: Select **`allocated_cost_usd`** $\rightarrow$ **`Descending`**.
4. On the right sidebar (**`STYLE`** tab):
   - Scroll down and check **`Show summary row`** (this automatically adds the `TOTAL` row at the bottom showing `$0.41`).

---

## 🎛️ Step 7: Add Top Filter Controls (30 seconds)

1. In the top menu toolbar, click **`Add a control`** $\rightarrow$ select **`Drop-down list`**.
2. Click above your scorecards to drop the filter button.
3. On the right sidebar (**`SETUP`** tab):
   - **Control field**: Select **`cost_center`**.
4. Add a second control for **`app_code`**.
5. Add a third control: click **`Add a control`** $\rightarrow$ select **`Date range control`** $\rightarrow$ place it in the top-right.

---

## 🎉 Done! Preview & Share

1. Click the blue **`View`** button in the top-right corner to see your live interactive dashboard!
   - Test clicking on any user or selecting a Cost Center from the dropdown: all charts filter instantly!
2. Click **`Share`** (top-right) $\rightarrow$ invite teammates or set **"Anyone with link can view"**.
