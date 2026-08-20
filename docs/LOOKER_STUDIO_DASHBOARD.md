# 📊 Looker Studio GenAI Governance Dashboard Recipes

**Audience:** FinOps Analysts, BI Developers, Executives  
**Purpose:** Step-by-step instructions to configure the Executive AI & GenAI Token Governance Dashboard in Google Looker Studio.

---

## 🎨 Dashboard Mockup & Executive Layout

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

## 🛠️ Step-by-Step Widget Configuration

### 1️⃣ KPI Scorecards
- **Total Tokens**: Metric: `SUM(total_tokens)`, Format: Compact (e.g. `148.2 M`).
- **Prompt Tokens**: Metric: `SUM(total_prompt_tokens)`, Format: Compact.
- **Candidate Output Tokens**: Metric: `SUM(total_output_tokens)`, Format: Compact.
- **Estimated Cost**: Metric: `SUM(estimated_cost_usd)`, Format: Currency USD `$`.

### 2️⃣ Top GenAI Consumers Leaderboard
- **Chart Type**: Table with Heatmap bars.
- **Dimension**: `user_id`.
- **Metrics**: `SUM(total_tokens)`, `SUM(estimated_cost_usd)`, `COUNT(total_requests)`.
- **Sort**: `SUM(total_tokens)` Descending.

### 3️⃣ Model Share Donut Chart
- **Chart Type**: Donut Chart (Hole radius 60%).
- **Dimension**: `model_name`.
- **Metric**: `SUM(total_tokens)`.
- **Slice Color**: Flash (Blue), Pro (Purple), Embedding (Green).

### 4️⃣ SAP Cost Center & App Code Financial Allocation Table
- **Chart Type**: Table.
- **Dimensions**: `cost_center`, `app_code`, `model_name`.
- **Metrics**: `SUM(total_prompt_tokens)`, `SUM(total_output_tokens)`, `SUM(estimated_cost_usd)`.
