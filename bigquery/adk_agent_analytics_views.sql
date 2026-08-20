-- ==============================================================================
-- 🧠 BigQuery DDL: ADK Agent Analytics & GenAI Governance Views
-- Dataset: `genai_finops_governance`
-- Table: `agent_events` (Native ADK BigQuery Storage Write API Table)
-- ==============================================================================

-- 1. View: Executive Scorecard KPIs
CREATE OR REPLACE VIEW `genai_finops_governance.v_adk_executive_kpis` AS
SELECT
  COUNT(DISTINCT session_id) AS total_agent_sessions,
  COUNTIF(event_type = 'LLM_RESPONSE') AS total_llm_turns,
  COUNTIF(event_type = 'TOOL_COMPLETED') AS total_tool_invocations,
  ROUND(SAFE_DIVIDE(COUNTIF(event_type = 'TOOL_COMPLETED' AND status = 'SUCCESS') * 100.0, 
                     COUNTIF(event_type = 'TOOL_COMPLETED')), 1) AS tool_success_rate_pct,
  SUM(COALESCE(prompt_tokens, 0)) AS total_prompt_tokens,
  SUM(COALESCE(cached_tokens, 0)) AS total_cached_tokens,
  SUM(COALESCE(output_tokens, 0)) AS total_output_tokens,
  SUM(COALESCE(total_tokens, 0)) AS grand_total_tokens,
  -- Estimated financial cost in USD
  ROUND(
    SUM(
      CASE 
        WHEN LOWER(model_name) LIKE '%flash%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00001875 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.000075 / 1000)
        WHEN LOWER(model_name) LIKE '%pro%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00125 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.00375 / 1000)
        ELSE (COALESCE(total_tokens, 0) * 0.000025 / 1000)
      END
    ), 2
  ) AS total_estimated_cost_usd
FROM `genai_finops_governance.agent_events`;

-- 2. View: User / Caller Token Leaderboard
CREATE OR REPLACE VIEW `genai_finops_governance.v_adk_user_leaderboard` AS
SELECT
  user_id,
  cost_center,
  app_code,
  app_name,
  COUNT(DISTINCT session_id) AS active_sessions,
  SUM(prompt_tokens) AS prompt_tokens,
  SUM(cached_tokens) AS cached_tokens,
  SUM(output_tokens) AS output_tokens,
  SUM(total_tokens) AS total_tokens,
  ROUND(
    SUM(
      CASE 
        WHEN LOWER(model_name) LIKE '%flash%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00001875 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.000075 / 1000)
        WHEN LOWER(model_name) LIKE '%pro%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00125 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.00375 / 1000)
        ELSE (COALESCE(total_tokens, 0) * 0.000025 / 1000)
      END
    ), 2
  ) AS estimated_cost_usd
FROM `genai_finops_governance.agent_events`
WHERE event_type = 'LLM_RESPONSE'
GROUP BY user_id, cost_center, app_code, app_name
ORDER BY total_tokens DESC;

-- 3. View: Model Family Unit Economics & Share
CREATE OR REPLACE VIEW `genai_finops_governance.v_adk_model_distribution` AS
SELECT
  model_name,
  COUNT(1) AS total_requests,
  SUM(total_tokens) AS total_tokens,
  ROUND(AVG(prompt_tokens), 1) AS avg_prompt_tokens_per_call,
  ROUND(AVG(output_tokens), 1) AS avg_output_tokens_per_call,
  ROUND(AVG(latency_ms), 1) AS avg_latency_ms,
  ROUND(
    SUM(
      CASE 
        WHEN LOWER(model_name) LIKE '%flash%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00001875 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.000075 / 1000)
        WHEN LOWER(model_name) LIKE '%pro%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00125 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.00375 / 1000)
        ELSE (COALESCE(total_tokens, 0) * 0.000025 / 1000)
      END
    ), 2
  ) AS total_cost_usd
FROM `genai_finops_governance.agent_events`
WHERE event_type = 'LLM_RESPONSE'
GROUP BY model_name
ORDER BY total_tokens DESC;

-- 4. View: SAP Cost Center & Application Code Financial Chargeback
CREATE OR REPLACE VIEW `genai_finops_governance.v_adk_cost_center_attribution` AS
SELECT
  cost_center,
  app_code,
  app_name,
  environment,
  COUNT(DISTINCT session_id) AS total_sessions,
  SUM(total_tokens) AS total_tokens,
  ROUND(
    SUM(
      CASE 
        WHEN LOWER(model_name) LIKE '%flash%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00001875 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.000075 / 1000)
        WHEN LOWER(model_name) LIKE '%pro%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00125 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.00375 / 1000)
        ELSE (COALESCE(total_tokens, 0) * 0.000025 / 1000)
      END
    ), 2
  ) AS allocated_cost_usd
FROM `genai_finops_governance.agent_events`
WHERE event_type = 'LLM_RESPONSE'
GROUP BY cost_center, app_code, app_name, environment
ORDER BY allocated_cost_usd DESC;

-- 5. View: Tool Invocations & Performance Diagnostics
CREATE OR REPLACE VIEW `genai_finops_governance.v_adk_tool_analytics` AS
SELECT
  tool_name,
  COUNT(1) AS total_invocations,
  COUNTIF(status = 'SUCCESS') AS successful_calls,
  COUNTIF(status = 'ERROR') AS failed_calls,
  ROUND(SAFE_DIVIDE(COUNTIF(status = 'SUCCESS') * 100.0, COUNT(1)), 1) AS success_rate_pct,
  ROUND(AVG(latency_ms), 1) AS avg_latency_ms,
  ROUND(MAX(latency_ms), 1) AS max_latency_ms
FROM `genai_finops_governance.agent_events`
WHERE event_type = 'TOOL_COMPLETED' AND tool_name IS NOT NULL
GROUP BY tool_name
ORDER BY total_invocations DESC;

-- 6. View: Daily Compliance & Token Consumption Trend
CREATE OR REPLACE VIEW `genai_finops_governance.v_adk_daily_trend` AS
SELECT
  DATE(CAST(timestamp AS TIMESTAMP)) AS usage_date,
  COUNT(DISTINCT session_id) AS daily_sessions,
  SUM(total_tokens) AS daily_tokens,
  ROUND(
    SUM(
      CASE 
        WHEN LOWER(model_name) LIKE '%flash%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00001875 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.000075 / 1000)
        WHEN LOWER(model_name) LIKE '%pro%' 
          THEN (COALESCE(prompt_tokens, 0) * 0.00125 / 1000) + 
               (COALESCE(output_tokens, 0) * 0.00375 / 1000)
        ELSE (COALESCE(total_tokens, 0) * 0.000025 / 1000)
      END
    ), 2
  ) AS daily_cost_usd
FROM `genai_finops_governance.agent_events`
WHERE event_type = 'LLM_RESPONSE'
GROUP BY usage_date
ORDER BY usage_date ASC;
