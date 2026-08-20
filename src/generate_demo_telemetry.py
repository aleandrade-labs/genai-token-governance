"""
Synthetic ADK BigQuery Agent Analytics Telemetry Generator (High-Volume Enterprise Scale)
Generates ~5,000 sessions and millions of tokens for Light S/A to populate BigQuery
and power the Looker Studio Executive Dashboard with large-scale data.
"""
import json
import random
import datetime

PROJECT_ID = "aleorg-dev-workload-01"
DATASET_ID = "genai_finops_governance"
TABLE_ID = "agent_events"

USERS = [
    {"user_id": "raphael_cano@light.com.br", "app_code": "cds-34199", "cost_center": "18207243", "app_name": "attendance_sac", "env": "prod"},
    {"user_id": "antonio_lameirao@light.com.br", "app_code": "cds-34242", "cost_center": "18207041", "app_name": "energy_watch_grid", "env": "prod"},
    {"user_id": "mariana_souza@light.com.br", "app_code": "cds-59339", "cost_center": "12272260", "app_name": "conexao_silvestre_pd", "env": "prod"},
    {"user_id": "carlos_eduardo@light.com.br", "app_code": "cds-77211", "cost_center": "18206922", "app_name": "smart_meter_rag", "env": "prod"},
    {"user_id": "equipe_transformacao@light.com.br", "app_code": "cds-91023", "cost_center": "18207115", "app_name": "substation_copilot", "env": "prod"},
    {"user_id": "lucas_mendes@light.com.br", "app_code": "cds-11045", "cost_center": "18207330", "app_name": "line_maintenance_ai", "env": "prod"},
    {"user_id": "beatriz_almeida@light.com.br", "app_code": "cds-88321", "cost_center": "18207455", "app_name": "energy_trading_analytics", "env": "prod"},
    {"user_id": "fernando_costa@light.com.br", "app_code": "cds-44102", "cost_center": "18207510", "app_name": "cyber_threat_detector", "env": "prod"},
    {"user_id": "sa-adk-automation@light.iam.gserviceaccount.com", "app_code": "cds-34199", "cost_center": "18207243", "app_name": "attendance_batch", "env": "prod"},
    {"user_id": "sa-grid-copilot@light.iam.gserviceaccount.com", "app_code": "cds-34242", "cost_center": "18207041", "app_name": "automated_grid_balancer", "env": "prod"},
    {"user_id": "sa-vertex-search@light.iam.gserviceaccount.com", "app_code": "cds-77211", "cost_center": "18206922", "app_name": "discovery_engine_indexer", "env": "prod"},
    {"user_id": "developer_sandbox@light.com.br", "app_code": "cds-19302", "cost_center": "18207800", "app_name": "hr_training_advisor", "env": "dev"}
]

MODELS = [
    {"name": "gemini-1.5-flash", "weight": 68, "prompt_rate": 0.00001875, "output_rate": 0.000075},
    {"name": "gemini-1.5-pro", "weight": 20, "prompt_rate": 0.00125, "output_rate": 0.00375},
    {"name": "gemini-2.0-flash", "weight": 7, "prompt_rate": 0.000025, "output_rate": 0.00010},
    {"name": "claude-3-5-sonnet", "weight": 3, "prompt_rate": 0.00300, "output_rate": 0.01500},
    {"name": "text-embedding-004", "weight": 2, "prompt_rate": 0.00001, "output_rate": 0.0}
]

TOOLS = [
    "query_substation_telemetry",
    "search_technical_manuals_rag",
    "calculate_feeder_overload",
    "check_smart_meter_billing_anomaly",
    "dispatch_field_crew_order",
    "estimate_loss_prevented",
    "query_scada_historian",
    "vertex_search_grounding"
]

def generate_enterprise_telemetry(num_sessions: int = 5000) -> list:
    rows = []
    end_date = datetime.datetime.now(datetime.timezone.utc)
    
    print(f"Generating {num_sessions} enterprise multi-turn agent sessions...")
    
    for session_idx in range(num_sessions):
        user_meta = random.choice(USERS)
        
        # Distribute over the past 30 days
        days_ago = random.uniform(0, 30)
        session_time = end_date - datetime.timedelta(days=days_ago)
        
        session_id = f"sess_{int(session_time.timestamp())}_{random.randint(10000, 99999)}"
        trace_id = f"trace_{random.randbytes(8).hex()}"
        
        model_choice = random.choices(MODELS, weights=[m["weight"] for m in MODELS])[0]
        model_name = model_choice["name"]
        
        # Number of turns in session (1 to 6)
        num_turns = random.randint(1, 6)
        
        for turn in range(1, num_turns + 1):
            turn_time = session_time + datetime.timedelta(seconds=turn * 4.2)
            span_root = f"span_{random.randbytes(6).hex()}"
            
            # Realistic token volume (compounding context in agent loops)
            base_prompt = random.randint(1200, 8500) * turn
            prompt_tokens = base_prompt
            cached_tokens = int(prompt_tokens * random.uniform(0.3, 0.75)) if turn > 1 else 0
            output_tokens = random.randint(200, 1800)
            total_tokens = prompt_tokens + output_tokens
            
            latency_ms = round(random.uniform(280.0, 1950.0), 1) if "flash" in model_name else round(random.uniform(1400.0, 4800.0), 1)
            
            # 1. LLM Generation Event
            rows.append({
                "trace_id": trace_id,
                "span_id": span_root,
                "parent_span_id": None,
                "event_type": "LLM_RESPONSE",
                "timestamp": turn_time.strftime('%Y-%m-%d %H:%M:%S'),
                "session_id": session_id,
                "turn_number": turn,
                "agent_name": f"{user_meta['app_name']}_agent",
                "model_name": model_name,
                "user_id": user_meta["user_id"],
                "cost_center": user_meta["cost_center"],
                "app_code": user_meta["app_code"],
                "app_name": user_meta["app_name"],
                "environment": user_meta["env"],
                "prompt_tokens": prompt_tokens,
                "cached_tokens": cached_tokens,
                "output_tokens": output_tokens,
                "total_tokens": total_tokens,
                "latency_ms": latency_ms,
                "status": "SUCCESS"
            })
            
            # 2. Tool Execution Event (75% probability per turn)
            if random.random() < 0.75:
                tool_name = random.choice(TOOLS)
                tool_latency = round(random.uniform(90.0, 720.0), 1)
                tool_status = "SUCCESS" if random.random() < 0.97 else "ERROR"
                
                rows.append({
                    "trace_id": trace_id,
                    "span_id": f"span_{random.randbytes(6).hex()}",
                    "parent_span_id": span_root,
                    "event_type": "TOOL_COMPLETED",
                    "timestamp": (turn_time + datetime.timedelta(seconds=1.4)).strftime('%Y-%m-%d %H:%M:%S'),
                    "session_id": session_id,
                    "turn_number": turn,
                    "agent_name": f"{user_meta['app_name']}_agent",
                    "model_name": model_name,
                    "user_id": user_meta["user_id"],
                    "cost_center": user_meta["cost_center"],
                    "app_code": user_meta["app_code"],
                    "app_name": user_meta["app_name"],
                    "environment": user_meta["env"],
                    "prompt_tokens": 0,
                    "cached_tokens": 0,
                    "output_tokens": 0,
                    "total_tokens": 0,
                    "latency_ms": tool_latency,
                    "tool_name": tool_name,
                    "status": tool_status
                })
                
    return rows

if __name__ == "__main__":
    records = generate_enterprise_telemetry(5000)
    print(f"Generated {len(records)} high-volume ADK telemetry events.")
    
    output_path = "bigquery/enterprise_large_events.jsonl"
    with open(output_path, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    print(f"Successfully saved to {output_path}")
