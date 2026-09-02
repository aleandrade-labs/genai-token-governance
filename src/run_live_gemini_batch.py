#!/usr/bin/env python3
"""
⚡ Live Gemini Batch Runner: Real Multi-Agent Token Generation on Vertex AI

Calls live Vertex AI Gemini models (Gemini 2.5 Flash, Gemini 2.5 Pro, Gemini 2.0 Flash)
with real domain-specific prompts for each agent in the "Light AI Value Transformation" catalog.
Captures genuine real-time `usage_metadata`, latency, cost, and streams live to BigQuery.

Usage:
  # Run 1 live turn for every transformation agent:
  python3 src/run_live_gemini_batch.py

  # Run multiple live rounds:
  python3 src/run_live_gemini_batch.py --rounds 3 --model gemini-2.5-flash
"""

import argparse
import datetime
import json
import os
import sys
import time
import uuid
from google import genai
from google.cloud import bigquery

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aleorg-dev-workload-01")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
DATASET_ID = "genai_finops_governance"
TABLE_ID = "agent_events"

# Live Prompt Test Suite for Transformation Agents
LIVE_AGENT_PROMPTS = [
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
        "default_model": "gemini-2.5-flash",
        "prompt": "Elabore uma proposta comercial de migração para o Mercado Livre de Energia (ACL) destacando economia de 25% na tarifa para uma indústria de médio porte no Rio de Janeiro."
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
        "default_model": "gemini-2.5-pro",
        "prompt": "Analise as cláusulas de penalidade por descumprimento de SLA em contrato de fornecimento de transformadores elétricos sob a regulação da ANEEL."
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
        "default_model": "gemini-2.5-flash",
        "prompt": "Crie um plano estruturado de capacitação técnica de eletricistas de rede para atuação em manutenção preventiva de linhas vivas com foco em segurança NR-10."
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
        "default_model": "gemini-2.5-flash",
        "prompt": "Escreva um manifesto Terraform para provisionar um cluster GKE Autopilot privado com Cloud NAT e Service Account dedicada no GCP."
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
        "default_model": "gemini-2.5-flash",
        "prompt": "Resuma o procedimento operacional padrão para manobra de isolamento de disjuntor em alimentador 138kV durante contingência climática."
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
        "default_model": "gemini-2.5-flash",
        "prompt": "Calcule a estimativa de economia obtida ao converter instâncias sob demanda em CUDs (Committed Use Discounts) de 3 anos para Compute Engine."
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
        "default_model": "gemini-2.5-pro",
        "prompt": "Sintetize um briefing executivo para o Conselho de Administração sobre o impacto da IA Generativa na redução de perdas não-técnicas e aumento da eficiência operacional."
    }
]

PRICING = {
    "gemini-2.5-flash": {"in": 0.075, "out": 0.30},
    "gemini-2.5-pro": {"in": 1.25, "out": 5.00},
    "gemini-2.0-flash": {"in": 0.10, "out": 0.40},
    "gemini-1.5-flash": {"in": 0.075, "out": 0.30},
    "gemini-1.5-pro": {"in": 1.25, "out": 5.00}
}

def execute_live_batch(rounds: int = 1, force_model: str = None):
    print("\n" + "═" * 85)
    print("🚀 \033[1;32mEXECUTING REAL LIVE GEMINI TOKEN GENERATION ON VERTEX AI\033[0m")
    print(f"   • Project ID       : {PROJECT_ID} (Region: {LOCATION})")
    print(f"   • Total Agents     : {len(LIVE_AGENT_PROMPTS)}")
    print(f"   • Rounds to Run    : {rounds}")
    print(f"   • Strategic Labels : `qualificado_como` (Receita/Transformacional/Corporativo/Core) | `valor` (Alto/Baixo)")
    print("═" * 85 + "\n")

    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    bq_client = bigquery.Client(project=PROJECT_ID)
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

    total_tokens_accum = 0
    total_cost_accum = 0.0
    rows_to_insert = []

    for round_idx in range(1, rounds + 1):
        print(f"\n🔄 --- STARTING ROUND {round_idx}/{rounds} ---")
        for agent_info in LIVE_AGENT_PROMPTS:
            model_name = force_model or agent_info["default_model"]
            print(f"\n🤖 \033[1;34m[{agent_info['agent_name']}]\033[0m | User: {agent_info['user_id']} | Model: \033[1;33m{model_name}\033[0m")
            print(f"   🏷️  Qualificado como: \033[1m{agent_info['qualificado_como']}\033[0m | Valor: \033[1m{agent_info['valor']}\033[0m | Budget: ${agent_info['budget_usd']:,.0f}")
            print(f"   📝 Prompt: \"{agent_info['prompt'][:80]}...\"")

            start_t = time.time()
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=agent_info["prompt"]
                )
                latency_ms = int((time.time() - start_t) * 1000)
                usage = response.usage_metadata

                prompt_tok = usage.prompt_token_count
                out_tok = usage.candidates_token_count
                thoughts_tok = getattr(usage, "thoughts_token_count", 0) or 0
                total_tok = usage.total_token_count

                pricing = PRICING.get(model_name, PRICING["gemini-2.5-flash"])
                cost = ((prompt_tok / 1_000_000.0) * pricing["in"]) + ((out_tok / 1_000_000.0) * pricing["out"])

                total_tokens_accum += total_tok
                total_cost_accum += cost

                now_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                session_id = f"sess_live_{int(time.time())}_{uuid.uuid4().hex[:6]}"
                trace_id = f"trace_{int(time.time())}_{uuid.uuid4().hex[:6]}"

                row = {
                    "trace_id": trace_id,
                    "span_id": f"span_{uuid.uuid4().hex[:6]}",
                    "parent_span_id": None,
                    "event_type": "LLM_RESPONSE",
                    "timestamp": now_str,
                    "session_id": session_id,
                    "turn_number": 1,
                    "agent_name": agent_info["agent_name"],
                    "model_name": model_name,
                    "user_id": agent_info["user_id"],
                    
                    # 🏷️ Customer Strategic Transformation Labels:
                    "qualificado_como": agent_info["qualificado_como"],
                    "valor": agent_info["valor"],
                    "budget_usd": agent_info["budget_usd"],
                    "token_errors": 0,

                    # 🏷️ 10 Customer Policy Tags:
                    "owner": agent_info["owner"],
                    "cost_center": agent_info["cost_center"],
                    "app_code": agent_info["app_code"],
                    "app_name": agent_info["app_name"],
                    "environment": agent_info["environment"],
                    "criticidade": agent_info["criticidade"],
                    "it_core": agent_info["it_core"],
                    "equipe_do_servico": agent_info["equipe_do_servico"],
                    "gerencia_responsavel": agent_info["gerencia_responsavel"],
                    "business_owner": agent_info["business_owner"],

                    # 🔢 Token Metrics:
                    "prompt_tokens": prompt_tok,
                    "cached_tokens": 0,
                    "output_tokens": out_tok,
                    "total_tokens": total_tok,
                    "latency_ms": float(latency_ms),
                    "status": "SUCCESS",
                    "tool_name": None
                }

                rows_to_insert.append(row)
                print(f"   ⏱️  {latency_ms} ms | 🔢 Prompt: {prompt_tok} | Output: {out_tok} | Total: \033[1;32m{total_tok:,} tokens\033[0m | 💰 ${cost:.6f} USD")
                print(f"   💬 Response Preview: {response.text[:120].strip()}...")

            except Exception as e:
                print(f"   ❌ Error calling Gemini: {e}")

    if rows_to_insert:
        print(f"\n📦 Streaming {len(rows_to_insert)} real-time events into BigQuery `{table_ref}`...")
        errors = bq_client.insert_rows_json(table_ref, rows_to_insert)
        if not errors:
            print("✅ All live agent events successfully synced to BigQuery!")
        else:
            print(f"⚠️ BigQuery insert notice: {errors}")

    print("\n" + "═" * 85)
    print("📈 \033[1;32mLIVE BATCH EXECUTION SUMMARY\033[0m:")
    print(f"   • Total Live Calls   : {len(rows_to_insert)}")
    print(f"   • Total Real Tokens  : \033[1m{total_tokens_accum:,}\033[0m")
    print(f"   • Total Real Cost    : \033[1m${total_cost_accum:.6f} USD\033[0m")
    print(f"   • BigQuery Table     : `{table_ref}`")
    print("═" * 85 + "\n")

def main():
    parser = argparse.ArgumentParser(description="Live Vertex AI Batch Token Generator for Transformation Agents")
    parser.add_argument("--rounds", type=int, default=1, help="Number of rounds to execute")
    parser.add_argument("--model", type=str, default=None, help="Force specific Gemini model (e.g. gemini-2.5-flash, gemini-2.5-pro)")
    args = parser.parse_args()

    execute_live_batch(rounds=args.rounds, force_model=args.model)

if __name__ == "__main__":
    main()
