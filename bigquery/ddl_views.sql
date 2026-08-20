-- ==============================================================================
-- 🧠 BigQuery DDL: GenAI Token & Cost Governance Views
-- Dataset: `genai_finops_governance`
-- ==============================================================================

-- 1. View: Token Consumption & Cost by User and Customer Policy Tags
CREATE OR REPLACE VIEW `genai_finops_governance.v_genai_token_consumption_by_user` AS
SELECT
  DATE(timestamp) AS usage_date,
  COALESCE(JSON_VALUE(jsonPayload.customLabels.user), JSON_VALUE(jsonPayload.user), 'service_account') AS user_id,
  JSON_VALUE(jsonPayload.customLabels.app_code) AS app_code,
  JSON_VALUE(jsonPayload.customLabels.cost_center) AS cost_center,
  COALESCE(JSON_VALUE(jsonPayload.model), JSON_VALUE(jsonPayload.model_name), 'gemini-1.5-flash') AS model_name,
  COUNT(1) AS total_requests,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64)) AS total_prompt_tokens,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.cachedContentTokenCount) AS INT64)) AS total_cached_tokens,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64)) AS total_output_tokens,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.totalTokenCount) AS INT64)) AS total_tokens,
  ROUND(
    SUM(
      CASE 
        WHEN LOWER(COALESCE(JSON_VALUE(jsonPayload.model), '')) LIKE '%flash%' 
          THEN (CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64) * 0.00001875 / 1000) + 
               (CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64) * 0.000075 / 1000)
        WHEN LOWER(COALESCE(JSON_VALUE(jsonPayload.model), '')) LIKE '%pro%' 
          THEN (CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64) * 0.00125 / 1000) + 
               (CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64) * 0.00375 / 1000)
        ELSE (CAST(JSON_VALUE(jsonPayload.usageMetadata.totalTokenCount) AS INT64) * 0.000025 / 1000)
      END
    ), 4
  ) AS estimated_cost_usd
FROM `genai_finops_governance.vertex_ai_request_logs`
GROUP BY usage_date, user_id, app_code, cost_center, model_name;

-- 2. View: Model Family Unit Economics & Cache Efficiency
CREATE OR REPLACE VIEW `genai_finops_governance.v_genai_model_unit_economics` AS
SELECT
  COALESCE(JSON_VALUE(jsonPayload.model), 'gemini-1.5-flash') AS model_name,
  COUNT(1) AS total_invocations,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64)), 1) AS avg_prompt_tokens,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.usageMetadata.candidatesTokenCount) AS INT64)), 1) AS avg_output_tokens,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.usageMetadata.totalTokenCount) AS INT64)), 1) AS avg_total_tokens,
  ROUND(SAFE_DIVIDE(SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.cachedContentTokenCount) AS INT64)), 
                     SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.promptTokenCount) AS INT64))) * 100, 2) AS cache_hit_rate_pct
FROM `genai_finops_governance.vertex_ai_request_logs`
GROUP BY model_name;

-- 3. View: Vertex AI Search Query Analytics
CREATE OR REPLACE VIEW `genai_finops_governance.v_vertex_search_query_analytics` AS
SELECT
  DATE(timestamp) AS search_date,
  resource.labels.project_id AS project_id,
  JSON_VALUE(jsonPayload.data_store_id) AS data_store_id,
  COALESCE(JSON_VALUE(jsonPayload.user), 'service_account') AS user_id,
  COUNT(1) AS total_search_queries,
  COUNTIF(JSON_VALUE(jsonPayload.summarySpec) IS NOT NULL) AS queries_with_generative_summary,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.latencyMs) AS FLOAT64)), 2) AS avg_latency_ms,
  ROUND(COUNT(1) * (5.0 / 1000), 4) AS search_cost_usd
FROM `genai_finops_governance.vertex_search_logs`
GROUP BY search_date, project_id, data_store_id, user_id;

-- 4. View: ADK Multi-Turn Agent Reasoning Governance
CREATE OR REPLACE VIEW `genai_finops_governance.v_adk_agent_governance` AS
SELECT
  DATE(timestamp) AS session_date,
  COALESCE(JSON_VALUE(jsonPayload.agent_name), 'default_agent') AS agent_name,
  COALESCE(JSON_VALUE(jsonPayload.tool_invoked), 'none') AS tool_name,
  JSON_VALUE(jsonPayload.customLabels.cost_center) AS cost_center,
  JSON_VALUE(jsonPayload.customLabels.app_code) AS app_code,
  COUNT(1) AS total_turns,
  SUM(CAST(JSON_VALUE(jsonPayload.usageMetadata.totalTokenCount) AS INT64)) AS total_tokens_spent,
  ROUND(AVG(CAST(JSON_VALUE(jsonPayload.latency_ms) AS FLOAT64)), 2) AS avg_latency_ms
FROM `genai_finops_governance.vertex_ai_request_logs`
WHERE JSON_VALUE(jsonPayload.event_type) = 'vertex_ai_generation'
GROUP BY session_date, agent_name, tool_name, cost_center, app_code;
