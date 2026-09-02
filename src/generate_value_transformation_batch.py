#!/usr/bin/env python3
"""
🚀 Big Batch Generator: Light AI Value Transformation & Token Governance

Populates BigQuery (`genai_finops_governance.agent_events`) with high-volume, realistic
workload sessions incorporating the customer's strategic categorization:
  - `qualificado_como`: Receita | Transformacional | Corporativo | Core
  - `valor`: Alto | Médio | Baixo
  - `agent_name`: Agent-Vendas, Agent-Juridico, Agent-RH, Agent-IT, Agent-Operacao,
                  FinOps-Analyst, Agent-Comunicacao, Agent-Onboarding, Executive-Agent, AI-Gov, AI-Agentic
  - `user_id`: Lucia, Evandro, Victor, Senna, Jesus, Lucero-Patrica, Vicente, Jose-Carlos, Jorge Sanchez, Omar, Juan
  - `budget_usd` & `token_errors`

Usage:
  # Generate standard enterprise batch (300 sessions, ~5M-10M tokens):
  python3 src/generate_value_transformation_batch.py

  # Generate massive scale batch (1,500 sessions across 30 days):
  python3 src/generate_value_transformation_batch.py --sessions 1500 --days 30
"""

import argparse
import datetime
import json
import os
import random
import sys
import tempfile
import time
from google.cloud import bigquery

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aleorg-dev-workload-01")
DATASET_ID = "genai_finops_governance"
TABLE_ID = "agent_events"

# 📋 Agents & Users from "Light AI Value Transformation" Sheet
TRANSFORMATION_AGENTS = [
    {
        "agent_name": "Agent-Vendas",
        "user_id": "lucia@light.com.br",
        "qualificado_como": "Receita",
        "valor": "Alto",
        "budget_usd": 20000.0,
        "cost_center": 18207041,
        "app_code": "cds-34242",
        "app_name": "vendas_energia",
        "owner": "comercial",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe_do_servico": "squad_vendas",
        "gerencia_responsavel": "gerencia_comercial",
        "business_owner": "lucia_mendes",
        "primary_model": "gemini-2.5-flash",
        "weight": 25 # High volume
    },
    {
        "agent_name": "Agent-Juridico",
        "user_id": "evandro@light.com.br",
        "qualificado_como": "Transformacional",
        "valor": "Alto",
        "budget_usd": 10000.0,
        "cost_center": 18206922,
        "app_code": "cds-77211",
        "app_name": "juridico_contratos",
        "owner": "juridico",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe_do_servico": "squad_juridico",
        "gerencia_responsavel": "gerencia_juridica",
        "business_owner": "evandro_costa",
        "primary_model": "gemini-2.5-pro", # Deep legal reasoning
        "weight": 15
    },
    {
        "agent_name": "Agent-RH",
        "user_id": "victor@light.com.br",
        "qualificado_como": "Corporativo",
        "valor": "Alto",
        "budget_usd": 40000.0,
        "cost_center": 18207243,
        "app_code": "cds-34199",
        "app_name": "rh_people_analytics",
        "owner": "rh",
        "environment": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe_do_servico": "squad_rh",
        "gerencia_responsavel": "gerencia_recursos_humanos",
        "business_owner": "victor_almeida",
        "primary_model": "gemini-2.5-flash",
        "weight": 10
    },
    {
        "agent_name": "Agent-IT",
        "user_id": "senna@light.com.br",
        "qualificado_como": "Corporativo",
        "valor": "Alto",
        "budget_usd": 10000.0,
        "cost_center": 18207115,
        "app_code": "cds-91023",
        "app_name": "it_devops_copilot",
        "owner": "arquitetura",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe_do_servico": "squad_cloud",
        "gerencia_responsavel": "gerencia_de_sistemas",
        "business_owner": "senna_silva",
        "primary_model": "gemini-2.5-pro",
        "weight": 12
    },
    {
        "agent_name": "Agent-Operacao",
        "user_id": "jesus@light.com.br",
        "qualificado_como": "Core",
        "valor": "Baixo",
        "budget_usd": 10000.0,
        "cost_center": 18207115,
        "app_code": "cds-91023",
        "app_name": "scada_grid_ops",
        "owner": "sistemas",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe_do_servico": "squad_alta_tensao",
        "gerencia_responsavel": "gerencia_de_operacoes",
        "business_owner": "jesus_rodriguez",
        "primary_model": "gemini-2.0-flash",
        "weight": 20
    },
    {
        "agent_name": "FinOps-Analyst",
        "user_id": "lucero_patricia@light.com.br",
        "qualificado_como": "Corporativo",
        "valor": "Alto",
        "budget_usd": 2000.0,
        "cost_center": 18207041,
        "app_code": "cds-34242",
        "app_name": "finops_cost_tracker",
        "owner": "arquitetura",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe_do_servico": "pdi-ew",
        "gerencia_responsavel": "gerencia_de_sistemas",
        "business_owner": "lucero_patricia",
        "primary_model": "gemini-2.5-flash",
        "weight": 8
    },
    {
        "agent_name": "Agent-Comunicacao",
        "user_id": "vicente@light.com.br",
        "qualificado_como": "Core",
        "valor": "Alto",
        "budget_usd": 2000.0,
        "cost_center": 18207243,
        "app_code": "cds-34199",
        "app_name": "comunicacao_institucional",
        "owner": "comunicacao",
        "environment": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe_do_servico": "squad_imprensa",
        "gerencia_responsavel": "gerencia_de_comunicacao",
        "business_owner": "vicente_lima",
        "primary_model": "gemini-2.5-flash",
        "weight": 6
    },
    {
        "agent_name": "Agent-Onboarding",
        "user_id": "jose_carlos@light.com.br",
        "qualificado_como": "Core",
        "valor": "Baixo",
        "budget_usd": 2010.0,
        "cost_center": 18207243,
        "app_code": "cds-34199",
        "app_name": "employee_onboarding",
        "owner": "rh",
        "environment": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe_do_servico": "squad_rh",
        "gerencia_responsavel": "gerencia_recursos_humanos",
        "business_owner": "jose_carlos",
        "primary_model": "gemini-1.5-flash",
        "weight": 5
    },
    {
        "agent_name": "Executive-Agent",
        "user_id": "jorge_sanchez@light.com.br",
        "qualificado_como": "Core",
        "valor": "Alto",
        "budget_usd": 2020.0,
        "cost_center": 18207041,
        "app_code": "cds-34242",
        "app_name": "c_level_briefing",
        "owner": "executivo",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe_do_servico": "squad_estrategia",
        "gerencia_responsavel": "diretoria_executiva",
        "business_owner": "jorge_sanchez",
        "primary_model": "gemini-2.5-pro",
        "weight": 7
    },
    {
        "agent_name": "AI-Gov",
        "user_id": "omar@light.com.br",
        "qualificado_como": "Core",
        "valor": "Alto",
        "budget_usd": 2023.0,
        "cost_center": 18207041,
        "app_code": "cds-34242",
        "app_name": "ai_governance_guardian",
        "owner": "arquitetura",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe_do_servico": "squad_governance",
        "gerencia_responsavel": "gerencia_de_sistemas",
        "business_owner": "omar_cardoso",
        "primary_model": "gemini-2.5-flash",
        "weight": 8
    },
    {
        "agent_name": "AI-Agentic",
        "user_id": "juan@light.com.br",
        "qualificado_como": "Core",
        "valor": "Alto",
        "budget_usd": 2026.0,
        "cost_center": 18207115,
        "app_code": "cds-91023",
        "app_name": "multi_agent_orchestrator",
        "owner": "pdi",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe_do_servico": "squad_ia_avancada",
        "gerencia_responsavel": "gerencia_transf_digital",
        "business_owner": "juan_perez",
        "primary_model": "gemini-2.5-pro",
        "weight": 10
    }
]

MODELS_CONFIG = {
    "gemini-2.5-flash": {"input_cost": 0.075, "output_cost": 0.30, "speed": "fast"},
    "gemini-2.5-pro": {"input_cost": 1.25, "output_cost": 5.00, "speed": "reasoning"},
    "gemini-2.0-flash": {"input_cost": 0.10, "output_cost": 0.40, "speed": "ultra_fast"},
    "gemini-1.5-flash": {"input_cost": 0.075, "output_cost": 0.30, "speed": "fast"},
    "gemini-1.5-pro": {"input_cost": 1.25, "output_cost": 5.00, "speed": "reasoning"}
}

TOOLS = [
    "search_knowledge_base_rag",
    "query_scada_historian",
    "sap_erp_billing_lookup",
    "legal_contract_analyzer",
    "hr_payroll_database",
    "gitops_pipeline_trigger",
    "substation_telemetry_fetch",
    "customer_satisfaction_scorer"
]

def generate_transformation_dataset(num_sessions: int = 500, days_window: int = 30) -> list:
    rows = []
    end_date = datetime.datetime.now(datetime.timezone.utc)
    weights = [a["weight"] for a in TRANSFORMATION_AGENTS]

    print(f"🚀 Generating {num_sessions:,} enterprise sessions across {days_window} days...")
    print(f"🏷️  Including labels: `qualificado_como` and `valor` from Light AI Value Transformation...")

    total_tokens = 0
    total_cost = 0.0

    for _ in range(num_sessions):
        app = random.choices(TRANSFORMATION_AGENTS, weights=weights)[0]
        days_ago = random.uniform(0, days_window)
        session_time = end_date - datetime.timedelta(days=days_ago)

        session_id = f"sess_transf_{int(session_time.timestamp())}_{random.randint(1000, 9999)}"
        trace_id = f"trace_{random.randbytes(8).hex()}"

        model = app["primary_model"]
        if random.random() < 0.15:
            model = random.choice(list(MODELS_CONFIG.keys()))

        turns = random.randint(1, 5)

        for turn in range(1, turns + 1):
            turn_time = session_time + datetime.timedelta(seconds=turn * 4.2)
            span_root = f"span_{random.randbytes(6).hex()}"

            if "pro" in model:
                prompt_tok = random.randint(3500, 28000)
                cached_tok = int(prompt_tok * random.uniform(0.3, 0.6)) if turn > 1 else 0
                out_tok = random.randint(600, 3500)
                latency = round(random.uniform(950.0, 3200.0), 1)
            else: # flash
                prompt_tok = random.randint(1200, 14000)
                cached_tok = int(prompt_tok * random.uniform(0.2, 0.5)) if turn > 1 else 0
                out_tok = random.randint(200, 1800)
                latency = round(random.uniform(180.0, 750.0), 1)

            tot_tok = prompt_tok + out_tok
            total_tokens += tot_tok

            # Calculate cost
            pricing = MODELS_CONFIG.get(model, MODELS_CONFIG["gemini-2.5-flash"])
            turn_cost = ((prompt_tok / 1_000_000.0) * pricing["input_cost"]) + ((out_tok / 1_000_000.0) * pricing["output_cost"])
            total_cost += turn_cost

            # Token error simulation (low frequency, matching sheet)
            has_token_error = 1 if random.random() < 0.03 else 0

            # 1. LLM Response Event
            rows.append({
                "trace_id": trace_id,
                "span_id": span_root,
                "parent_span_id": None,
                "event_type": "LLM_RESPONSE",
                "timestamp": turn_time.strftime("%Y-%m-%d %H:%M:%S"),
                "session_id": session_id,
                "turn_number": turn,
                "agent_name": app["agent_name"],
                "model_name": model,
                "user_id": app["user_id"],
                
                # 🏷️ Customer Strategic Value Labels:
                "qualificado_como": app["qualificado_como"],
                "valor": app["valor"],
                "budget_usd": app["budget_usd"],
                "token_errors": has_token_error,

                # 🏷️ 10 Customer Policy Tags:
                "owner": app["owner"],
                "cost_center": app["cost_center"],
                "app_code": app["app_code"],
                "app_name": app["app_name"],
                "environment": app["environment"],
                "criticidade": app["criticidade"],
                "it_core": app["it_core"],
                "equipe_do_servico": app["equipe_do_servico"],
                "gerencia_responsavel": app["gerencia_responsavel"],
                "business_owner": app["business_owner"],

                # 🔢 Token Metrics:
                "prompt_tokens": prompt_tok,
                "cached_tokens": cached_tok,
                "output_tokens": out_tok,
                "total_tokens": tot_tok,
                "latency_ms": latency,
                "status": "SUCCESS" if not has_token_error else "ERROR",
                "tool_name": None
            })

            # 2. Tool Execution (60% probability)
            if random.random() < 0.60:
                tool_name = random.choice(TOOLS)
                tool_latency = round(random.uniform(50.0, 380.0), 1)

                rows.append({
                    "trace_id": trace_id,
                    "span_id": f"span_{random.randbytes(6).hex()}",
                    "parent_span_id": span_root,
                    "event_type": "TOOL_COMPLETED",
                    "timestamp": (turn_time + datetime.timedelta(seconds=1.5)).strftime("%Y-%m-%d %H:%M:%S"),
                    "session_id": session_id,
                    "turn_number": turn,
                    "agent_name": app["agent_name"],
                    "model_name": model,
                    "user_id": app["user_id"],
                    
                    "qualificado_como": app["qualificado_como"],
                    "valor": app["valor"],
                    "budget_usd": app["budget_usd"],
                    "token_errors": 0,

                    "owner": app["owner"],
                    "cost_center": app["cost_center"],
                    "app_code": app["app_code"],
                    "app_name": app["app_name"],
                    "environment": app["environment"],
                    "criticidade": app["criticidade"],
                    "it_core": app["it_core"],
                    "equipe_do_servico": app["equipe_do_servico"],
                    "gerencia_responsavel": app["gerencia_responsavel"],
                    "business_owner": app["business_owner"],

                    "prompt_tokens": 0,
                    "cached_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "latency_ms": tool_latency,
                    "status": "SUCCESS",
                    "tool_name": tool_name
                })

    print(f"✨ Generated {len(rows):,} total telemetry events!")
    print(f"🔢 Total Simulated Tokens : {total_tokens:,}")
    print(f"💰 Total Estimated Cost   : ${total_cost:,.2f} USD\n")
    return rows

def load_to_bigquery_batch(rows: list):
    client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    print(f"📦 Streaming {len(rows):,} rows into BigQuery table `{table_ref}` using batch JSONL load...")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
        temp_path = f.name

    try:
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION],
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND
        )

        with open(temp_path, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

        print("⏳ Waiting for BigQuery load job to complete...")
        job.result()
        print(f"✅ Successfully loaded {len(rows):,} events into `{table_ref}`!\n")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def update_looker_analytical_views():
    """
    Creates/updates the unified Looker Studio analytical view exposing `qualificado_como` and `valor`.
    """
    client = bigquery.Client(project=PROJECT_ID)
    print("🔄 Updating Looker Studio analytical views with `qualificado_como` & `valor` dimensions...")

    sql_view = f"""
    CREATE OR REPLACE VIEW `{PROJECT_ID}.{DATASET_ID}.v_value_transformation_dashboard` AS
    SELECT
      timestamp,
      DATE(timestamp) as event_date,
      session_id,
      trace_id,
      event_type,
      agent_name,
      model_name,
      user_id,
      
      -- 🏷️ Strategic Value Transformation Dimensions:
      COALESCE(qualificado_como, 'Core') AS qualificado_como,
      COALESCE(valor, 'Alto') AS valor,
      budget_usd,
      token_errors,

      -- 🏷️ 10 Customer Policy Tags:
      owner,
      cost_center,
      app_code,
      app_name,
      environment,
      criticidade,
      it_core,
      equipe_do_servico,
      gerencia_responsavel,
      business_owner,

      -- 🔢 Token & Latency Metrics:
      prompt_tokens,
      cached_tokens,
      output_tokens,
      total_tokens,
      latency_ms,
      status,
      tool_name,

      -- 💰 Calculated Cost in USD:
      CASE 
        WHEN model_name LIKE '%2.5-pro%' THEN ((prompt_tokens / 1000000.0) * 1.25) + ((output_tokens / 1000000.0) * 5.00)
        WHEN model_name LIKE '%2.5-flash%' THEN ((prompt_tokens / 1000000.0) * 0.075) + ((output_tokens / 1000000.0) * 0.30)
        WHEN model_name LIKE '%2.0-flash%' THEN ((prompt_tokens / 1000000.0) * 0.10) + ((output_tokens / 1000000.0) * 0.40)
        WHEN model_name LIKE '%1.5-pro%' THEN ((prompt_tokens / 1000000.0) * 1.25) + ((output_tokens / 1000000.0) * 5.00)
        ELSE ((prompt_tokens / 1000000.0) * 0.075) + ((output_tokens / 1000000.0) * 0.30)
      END AS estimated_cost_usd

    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    """

    job = client.query(sql_view)
    job.result()
    print(f"✅ View `{PROJECT_ID}.{DATASET_ID}.v_value_transformation_dashboard` created/updated successfully!\n")

def main():
    parser = argparse.ArgumentParser(description="Generate Big Batch of Light AI Value Transformation Telemetry")
    parser.add_argument("--sessions", type=int, default=400, help="Number of multi-turn user sessions to generate")
    parser.add_argument("--days", type=int, default=30, help="Time window in days")
    parser.add_argument("--dry-run", action="store_true", help="Generate without loading into BigQuery")
    args = parser.parse_args()

    rows = generate_transformation_dataset(num_sessions=args.sessions, days_window=args.days)
    
    if not args.dry_run:
        load_to_bigquery_batch(rows)
        update_looker_analytical_views()
    else:
        print("💡 Dry-run mode: BigQuery load skipped.")

if __name__ == "__main__":
    main()
