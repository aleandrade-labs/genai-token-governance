"""
High-Volume Enterprise ADK Token & Policy Governance Generator
Generates realistic multi-turn agent workloads across modern Gemini models 
(Gemini 2.5, Gemini 2.0, Gemini 1.5) with all 10 Customer Policy Tags from Light S/A.
"""
import argparse
import json
import random
import datetime
import os
import tempfile
from google.cloud import bigquery

PROJECT_ID = "aleorg-dev-workload-01"
DATASET_ID = "genai_finops_governance"
TABLE_ID = "agent_events"

# 🏢 Enterprise Applications mapped 1-to-1 with customer_policy_tags.csv
APPLICATIONS = [
    {
        "app_code": "cds-34242",
        "cost_center": "18207041",
        "app_name": "energy_watch_grid",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe": "pdi-ew",
        "gerencia": "gerencia_de_sistemas",
        "business_owner": "raphael_cano",
        "agent": "energy_watch_agent"
    },
    {
        "app_code": "cds-59339",
        "cost_center": "12272260",
        "app_name": "conexao_silvestre_pd",
        "owner": "pdi",
        "env": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe": "equipe_pdi_conexao_silvestre",
        "gerencia": "coordenacao_projetos_pdi",
        "business_owner": "alexandrade",
        "agent": "conexao_silvestre_agent"
    },
    {
        "app_code": "cds-91023",
        "cost_center": "18207115",
        "app_name": "substation_copilot",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe": "equipe_transformacao_digital",
        "gerencia": "gerencia_de_transformacao_digital",
        "business_owner": "antonio_lameirao",
        "agent": "substation_copilot_agent"
    },
    {
        "app_code": "cds-34199",
        "cost_center": "18207243",
        "app_name": "attendance_sac",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe": "equipe_attendance",
        "gerencia": "gerencia_de_transformacao_digital",
        "business_owner": "mariana_souza",
        "agent": "attendance_agent"
    },
    {
        "app_code": "cds-77211",
        "cost_center": "18206922",
        "app_name": "smart_meter_rag",
        "owner": "sistemas",
        "env": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe": "equipe_smartreader",
        "gerencia": "gerencia_de_sistemas",
        "business_owner": "raphael_cano",
        "agent": "smart_meter_agent"
    },
    {
        "app_code": "cds-34302",
        "cost_center": "18207243",
        "app_name": "light_plus",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe": "equipe_light_plus",
        "gerencia": "gerencia_de_transformacao_digital",
        "business_owner": "antonio_lameirao",
        "agent": "light_plus_assistant"
    },
    {
        "app_code": "cds-34270",
        "cost_center": "18207243",
        "app_name": "gdis_distribution",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe": "equipe_gdis",
        "gerencia": "gerencia_de_sistemas",
        "business_owner": "carlos_alberto",
        "agent": "gdis_grid_agent"
    },
    {
        "app_code": "cds-99107",
        "cost_center": "18207041",
        "app_name": "chinese_wall_integracao",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe": "equipe_chinese_wall",
        "gerencia": "gerencia_de_transformacao_digital",
        "business_owner": "raphael_cano",
        "agent": "integration_hub_agent"
    },
    {
        "app_code": "cds-101860",
        "cost_center": "18207243",
        "app_name": "manejo_vegetal",
        "owner": "sistemas",
        "env": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe": "equipe_manejo_vegetal",
        "gerencia": "gerencia_de_sistemas",
        "business_owner": "fernando_costa",
        "agent": "vegetation_hazard_detector"
    },
    {
        "app_code": "cds-52878",
        "cost_center": "18207188",
        "app_name": "monitoramento_orbital",
        "owner": "sistemas",
        "env": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe": "pdi-orbital",
        "gerencia": "coordenacao_projetos_pdi",
        "business_owner": "raphael_cano",
        "agent": "satellite_vision_copilot"
    },
    {
        "app_code": "cds-80405",
        "cost_center": "18207243",
        "app_name": "databricks_lakehouse",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe": "equipe_de_dados",
        "gerencia": "gerencia_de_transformacao_digital",
        "business_owner": "alexandrade",
        "agent": "lakehouse_sql_agent"
    },
    {
        "app_code": "cds-101807",
        "cost_center": "18207243",
        "app_name": "n8n_automation_rpa",
        "owner": "arquitetura",
        "env": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe": "equipe_de_automacao_rpa_e_ia",
        "gerencia": "gerencia_de_transformacao_digital",
        "business_owner": "alexandrade",
        "agent": "rpa_workflow_agent"
    }
]

# 👤 Enterprise Identities
USERS = [
    "admin@alexandrade.altostrat.com",
    "alexandrade@google.com",
    "sa-finops-label-governance@aleorg-dev-workload-01.iam.gserviceaccount.com",
    "raphael.cano@light.com.br",
    "antonio.lameirao@light.com.br",
    "mariana.souza@light.com.br",
    "carlos.alberto@light.com.br"
]

# 🤖 Modern Gemini Model Family
MODELS = [
    {"name": "gemini-2.5-flash", "weight": 40},
    {"name": "gemini-2.0-flash", "weight": 25},
    {"name": "gemini-2.5-pro", "weight": 15},
    {"name": "gemini-1.5-pro", "weight": 12},
    {"name": "gemini-1.5-flash", "weight": 5},
    {"name": "text-embedding-005", "weight": 3}
]

TOOLS = [
    "query_substation_status",
    "calculate_feeder_loss",
    "search_customer_history",
    "query_substation_telemetry",
    "check_smart_meter_billing_anomaly",
    "search_technical_manuals_rag",
    "dispatch_field_crew_order",
    "estimate_loss_prevented",
    "query_scada_historian",
    "satellite_vegetation_analysis",
    "vertex_search_grounding"
]

def generate_telemetry_dataset(num_sessions: int = 150, days_window: int = 30) -> list:
    rows = []
    end_date = datetime.datetime.now(datetime.timezone.utc)
    
    print(f"🚀 Generating {num_sessions:,} enterprise sessions across {days_window} days...")
    total_tokens = 0
    
    for _ in range(num_sessions):
        app = random.choice(APPLICATIONS)
        user = random.choice(USERS)
        
        days_ago = random.uniform(0, days_window)
        session_time = end_date - datetime.timedelta(days=days_ago)
        
        session_id = f"sess_{int(session_time.timestamp())}_{random.randint(1000, 9999)}"
        trace_id = f"trace_{random.randbytes(8).hex()}"
        
        model = random.choices(MODELS, weights=[m["weight"] for m in MODELS])[0]["name"]
        turns = random.randint(1, 4)
        
        for turn in range(1, turns + 1):
            turn_time = session_time + datetime.timedelta(seconds=turn * 3.5)
            span_root = f"span_{random.randbytes(6).hex()}"
            
            if "embedding" in model:
                prompt_tok = random.randint(300, 1800)
                cached_tok = 0
                out_tok = 0
                latency = round(random.uniform(45.0, 150.0), 1)
            elif "pro" in model:
                prompt_tok = random.randint(4500, 24000)
                cached_tok = int(prompt_tok * random.uniform(0.3, 0.7)) if turn > 1 else 0
                out_tok = random.randint(800, 3200)
                latency = round(random.uniform(1200.0, 3800.0), 1)
            else: # flash
                prompt_tok = random.randint(1800, 12000)
                cached_tok = int(prompt_tok * random.uniform(0.2, 0.6)) if turn > 1 else 0
                out_tok = random.randint(250, 1500)
                latency = round(random.uniform(220.0, 850.0), 1)
                
            tot_tok = prompt_tok + out_tok
            total_tokens += tot_tok
            
            # 1. LLM Generation
            rows.append({
                "trace_id": trace_id,
                "span_id": span_root,
                "parent_span_id": None,
                "event_type": "LLM_RESPONSE",
                "timestamp": turn_time.strftime("%Y-%m-%d %H:%M:%S"),
                "session_id": session_id,
                "turn_number": turn,
                "agent_name": app["agent"],
                "model_name": model,
                "user_id": user,
                # 🏷️ 10 Customer Policy Tags
                "owner": app["owner"],
                "cost_center": app["cost_center"],
                "app_code": app["app_code"],
                "app_name": app["app_name"],
                "environment": app["env"],
                "criticidade": app["criticidade"],
                "it_core": app["it_core"],
                "equipe_do_servico": app["equipe"],
                "gerencia_responsavel": app["gerencia"],
                "business_owner": app["business_owner"],
                # Token Metrics
                "prompt_tokens": prompt_tok,
                "cached_tokens": cached_tok,
                "output_tokens": out_tok,
                "total_tokens": tot_tok,
                "latency_ms": latency,
                "status": "SUCCESS"
            })
            
            # 2. Tool Execution (70% probability)
            if random.random() < 0.70 and "embedding" not in model:
                tool_name = random.choice(TOOLS)
                tool_latency = round(random.uniform(60.0, 480.0), 1)
                tool_status = "SUCCESS" if random.random() < 0.98 else "ERROR"
                
                rows.append({
                    "trace_id": trace_id,
                    "span_id": f"span_{random.randbytes(6).hex()}",
                    "parent_span_id": span_root,
                    "event_type": "TOOL_COMPLETED",
                    "timestamp": (turn_time + datetime.timedelta(seconds=1.2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "session_id": session_id,
                    "turn_number": turn,
                    "agent_name": app["agent"],
                    "model_name": model,
                    "user_id": user,
                    # 🏷️ 10 Customer Policy Tags
                    "owner": app["owner"],
                    "cost_center": app["cost_center"],
                    "app_code": app["app_code"],
                    "app_name": app["app_name"],
                    "environment": app["env"],
                    "criticidade": app["criticidade"],
                    "it_core": app["it_core"],
                    "equipe_do_servico": app["equipe"],
                    "gerencia_responsavel": app["gerencia"],
                    "business_owner": app["business_owner"],
                    # Token Metrics
                    "prompt_tokens": 0,
                    "cached_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "latency_ms": tool_latency,
                    "tool_name": tool_name,
                    "status": tool_status
                })
                
    print(f"✨ Successfully generated {len(rows):,} events across {num_sessions:,} sessions.")
    print(f"🔢 Total Simulated Tokens: {total_tokens:,} ({total_tokens / 1_000_000:.2f} Million Tokens)")
    return rows

def load_into_bigquery(rows: list, append: bool = True):
    bq_client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as tmp_file:
        for r in rows:
            tmp_file.write(json.dumps(r) + "\n")
        tmp_path = tmp_file.name
        
    try:
        print(f"\n📤 Loading {len(rows):,} events into BigQuery `{table_ref}` via Batch Load Job...")
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND if append else bigquery.WriteDisposition.WRITE_TRUNCATE,
            schema_update_options=[bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION]
        )
        
        with open(tmp_path, "rb") as source_file:
            job = bq_client.load_table_from_file(source_file, table_ref, job_config=job_config)
            job.result()
            
        print("🎉 SUCCESS: High-volume enterprise telemetry loaded into BigQuery!")
        print("👉 Go to Looker Studio and click 'Refresh data' to see the updated figures!")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate high-volume modern Gemini tokens into BigQuery")
    parser.add_argument("--sessions", type=int, default=120, help="Number of agent sessions (e.g. 100, 250, 500)")
    parser.add_argument("--days", type=int, default=30, help="Historical time window in days (default: 30)")
    parser.add_argument("--clear", action="store_true", help="Clear past table data before loading")
    
    args = parser.parse_args()
    
    dataset = generate_telemetry_dataset(num_sessions=args.sessions, days_window=args.days)
    load_into_bigquery(dataset, append=not args.clear)
