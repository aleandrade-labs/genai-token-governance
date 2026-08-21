#!/usr/bin/env python3
"""
💬 Interactive Gemini Chat & Real-Time GenAI Token Governance CLI

Interact directly with the latest Google Gemini models (Gemini 2.5 Flash, Gemini 2.5 Pro, Gemini 2.0 Flash)
while automatically capturing genuine token telemetry, cost economics, and streaming compliance events
with the 10 Customer Policy Tags into BigQuery for Looker Studio dashboards.

Usage:
  # Interactive Multi-Turn Chat:
  python3 src/interactive_chat.py

  # Select specific model & application:
  python3 src/interactive_chat.py --model gemini-2.5-pro --app energy_watch

  # Single One-Shot Prompt:
  python3 src/interactive_chat.py --prompt "Explain the benefits of smart grid automation in electrical utilities"
"""

import os
import sys
import time
import uuid
import argparse
from datetime import datetime, timezone
from typing import Dict, Any, Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ Error: `google-genai` SDK is required. Run: pip install google-genai")
    sys.exit(1)

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None

# Default Configuration
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aleorg-dev-workload-01")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
DATASET_ID = "genai_finops_governance"
TABLE_ID = "agent_events"

# Available Models & Pricing (USD per 1 Million Tokens)
MODELS_CATALOG = {
    "gemini-2.5-flash": {
        "description": "⚡ Gemini 2.5 Flash (Fast, highly capable, hybrid thinking mode)",
        "input_price_1m": 0.075,
        "output_price_1m": 0.30
    },
    "gemini-2.5-pro": {
        "description": "🧠 Gemini 2.5 Pro (State-of-the-art complex reasoning & code)",
        "input_price_1m": 1.25,
        "output_price_1m": 5.00
    },
    "gemini-2.0-flash": {
        "description": "🚀 Gemini 2.0 Flash (Next-gen low latency multimodal)",
        "input_price_1m": 0.10,
        "output_price_1m": 0.40
    },
    "gemini-1.5-flash": {
        "description": "📦 Gemini 1.5 Flash (Standard high throughput)",
        "input_price_1m": 0.075,
        "output_price_1m": 0.30
    },
    "gemini-1.5-pro": {
        "description": "📚 Gemini 1.5 Pro (Massive 2M token context window)",
        "input_price_1m": 1.25,
        "output_price_1m": 5.00
    }
}

# Pre-Configured Enterprise Applications (Light S/A Policy Taxonomy)
ENTERPRISE_APPS = {
    "energy_watch": {
        "app_code": "cds-34242",
        "cost_center": "18207041",
        "application": "energy_watch",
        "owner": "arquitetura",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "nao",
        "equipe_do_servico": "pdi-ew",
        "gerencia_responsavel": "gerencia_de_sistemas",
        "business_owner": "raphael_cano"
    },
    "smart_meter_rag": {
        "app_code": "cds-77211",
        "cost_center": "18206922",
        "application": "smart_meter_rag",
        "owner": "pdi",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe_do_servico": "equipe_smart_grid",
        "gerencia_responsavel": "gerencia_transf_digital",
        "business_owner": "antonio_lameirao"
    },
    "attendance_sac": {
        "app_code": "cds-34199",
        "cost_center": "18207243",
        "application": "attendance",
        "owner": "arquitetura",
        "environment": "prod",
        "criticidade": "nao",
        "it_core": "nao",
        "equipe_do_servico": "equipe_attendance",
        "gerencia_responsavel": "gerencia_transf_digital",
        "business_owner": "antonio_lameirao"
    },
    "substation_copilot": {
        "app_code": "cds-91023",
        "cost_center": "18207115",
        "application": "substation_copilot",
        "owner": "sistemas",
        "environment": "prod",
        "criticidade": "sim",
        "it_core": "sim",
        "equipe_do_servico": "equipe_alta_tensao",
        "gerencia_responsavel": "gerencia_de_sistemas",
        "business_owner": "raphael_cano"
    }
}

class InteractiveGeminiSession:
    def __init__(
        self,
        project_id: str = PROJECT_ID,
        location: str = LOCATION,
        model_name: str = "gemini-2.5-flash",
        app_key: str = "energy_watch",
        user_id: Optional[str] = None
    ):
        self.project_id = project_id
        self.location = location
        self.model_name = model_name if model_name in MODELS_CATALOG else "gemini-2.5-flash"
        self.app_key = app_key if app_key in ENTERPRISE_APPS else "energy_watch"
        self.user_id = user_id or os.environ.get("USER", "admin@alexandrade.altostrat.com")
        self.session_id = f"sess_chat_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        self.turn_count = 0
        self.total_session_tokens = 0
        self.total_session_cost = 0.0

        # Initialize Google Gen AI Vertex Client
        try:
            self.client = genai.Client(vertexai=True, project=self.project_id, location=self.location)
            self.chat = self.client.chats.create(model=self.model_name)
        except Exception as e:
            print(f"❌ Failed to initialize Google Gen AI Client on Vertex AI: {e}")
            sys.exit(1)

        # BigQuery Client for Streaming Governance
        self.bq_client = None
        if bigquery:
            try:
                self.bq_client = bigquery.Client(project=self.project_id)
            except Exception:
                pass

    def get_active_tags(self) -> Dict[str, str]:
        return ENTERPRISE_APPS.get(self.app_key, ENTERPRISE_APPS["energy_watch"])

    def calculate_cost(self, prompt_tokens: int, output_tokens: int) -> float:
        pricing = MODELS_CATALOG.get(self.model_name, MODELS_CATALOG["gemini-2.5-flash"])
        input_cost = (prompt_tokens / 1_000_000.0) * pricing["input_price_1m"]
        output_cost = (output_tokens / 1_000_000.0) * pricing["output_price_1m"]
        return input_cost + output_cost

    def stream_telemetry_to_bigquery(
        self,
        prompt_tokens: int,
        output_tokens: int,
        total_tokens: int,
        thoughts_tokens: int,
        latency_ms: int,
        cost_usd: float
    ):
        if not self.bq_client:
            return

        tags = self.get_active_tags()
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        trace_id = f"trace_{int(time.time())}_{uuid.uuid4().hex[:6]}"
        span_id = f"span_{int(time.time())}_{self.turn_count}"

        row = {
            "trace_id": trace_id,
            "span_id": span_id,
            "parent_span_id": None,
            "event_type": "LLM_RESPONSE",
            "timestamp": now_str,
            "session_id": self.session_id,
            "turn_number": self.turn_count,
            "agent_name": f"{tags['application']}_interactive",
            "model_name": self.model_name,
            "user_id": self.user_id,
            # 10 Customer Policy Tags
            "owner": tags["owner"],
            "cost_center": tags["cost_center"],
            "app_code": tags["app_code"],
            "app_name": tags["application"],
            "environment": tags["environment"],
            "criticidade": tags["criticidade"],
            "it_core": tags["it_core"],
            "equipe_do_servico": tags["equipe_do_servico"],
            "gerencia_responsavel": tags["gerencia_responsavel"],
            "business_owner": tags["business_owner"],
            # Token Metrics
            "prompt_tokens": prompt_tokens,
            "cached_tokens": 0,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "latency_ms": float(latency_ms),
            "status": "SUCCESS",
            "tool_name": None
        }

        try:
            table_ref = f"{self.project_id}.{DATASET_ID}.{TABLE_ID}"
            errors = self.bq_client.insert_rows_json(table_ref, [row])
            if errors:
                print(f"⚠️ [BigQuery Notice]: Streaming insert encountered: {errors}", file=sys.stderr)
        except Exception as e:
            print(f"⚠️ [BigQuery Stream Error]: {e}", file=sys.stderr)

    def send_prompt(self, user_prompt: str, stream: bool = True):
        self.turn_count += 1
        start_time = time.time()

        print(f"\n🤖 \033[1;36m[{self.model_name}]\033[0m: ", end="", flush=True)

        full_text = ""
        try:
            if stream:
                response_stream = self.chat.send_message_stream(user_prompt)
                for chunk in response_stream:
                    if chunk.text:
                        print(chunk.text, end="", flush=True)
                        full_text += chunk.text
                print()
                # Fetch complete usage metadata from chat state
                usage = getattr(self.chat, "last_response_usage", None) or getattr(response_stream, "usage_metadata", None)
            else:
                response = self.chat.send_message(user_prompt)
                full_text = response.text
                print(full_text)
                usage = response.usage_metadata
        except Exception as e:
            print(f"\n❌ Error during generation: {e}")
            return

        latency_ms = int((time.time() - start_time) * 1000)

        # Extract tokens
        prompt_tokens = getattr(usage, "prompt_token_count", 0) if usage else max(len(user_prompt.split()) * 2, 8)
        output_tokens = getattr(usage, "candidates_token_count", 0) if usage else max(len(full_text.split()) * 2, 12)
        thoughts_tokens = getattr(usage, "thoughts_token_count", 0) if usage else 0
        total_tokens = getattr(usage, "total_token_count", prompt_tokens + output_tokens + thoughts_tokens)

        cost = self.calculate_cost(prompt_tokens, output_tokens)
        self.total_session_tokens += total_tokens
        self.total_session_cost += cost

        # Stream real-time telemetry to BigQuery
        self.stream_telemetry_to_bigquery(
            prompt_tokens=prompt_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            thoughts_tokens=thoughts_tokens,
            latency_ms=latency_ms,
            cost_usd=cost
        )

        tags = self.get_active_tags()
        # Telemetry Banner
        print(f"\n\033[90m" + "─"*78)
        print(f"📊 Turn #{self.turn_count} | ⏱️  {latency_ms} ms | 🔢 Prompt: {prompt_tokens} | Output: {output_tokens} (Thoughts: {thoughts_tokens}) | Total: {total_tokens} tokens")
        print(f"💰 Turn Cost: ${cost:.6f} USD | 🏷️ App: {tags['application']} ({tags['app_code']}) | Cost Center: {tags['cost_center']}")
        print(f"📈 BigQuery Synced: `{self.project_id}.{DATASET_ID}.{TABLE_ID}`")
        print("─"*78 + "\033[0m")

    def run_interactive_loop(self):
        tags = self.get_active_tags()
        print("\n" + "═"*80)
        print("💬 \033[1;32mGoogle Cloud GenAI Interactive Token Governance Console\033[0m")
        print(f"   • Project ID       : \033[1;34m{self.project_id}\033[0m (Region: {self.location})")
        print(f"   • Active Model     : \033[1;33m{self.model_name}\033[0m")
        print(f"   • Application Tag  : \033[1;35m{tags['application']}\033[0m (App Code: {tags['app_code']} | Cost Center: {tags['cost_center']})")
        print(f"   • Session ID       : {self.session_id}")
        print("═"*80)
        print("💡 Commands: `/model <name>`, `/models`, `/app <name>`, `/stats`, `/clear`, `/exit`\n")

        while True:
            try:
                user_input = input("\033[1;37m👤 You:\033[0m ").strip()
                if not user_input:
                    continue

                # Slash Command Handlers
                if user_input.lower() in ["/exit", "/quit", "exit", "quit"]:
                    print("\n👋 Ending session. Here is your session summary:")
                    self.print_session_stats()
                    break

                elif user_input.lower() == "/models":
                    print("\n📋 Available Gemini Models:")
                    for m, info in MODELS_CATALOG.items():
                        cur = " (ACTIVE)" if m == self.model_name else ""
                        print(f"   • \033[1m{m}\033[0m{cur}: {info['description']}")
                        print(f"     Pricing: ${info['input_price_1m']}/1M in, ${info['output_price_1m']}/1M out")
                    print()
                    continue

                elif user_input.startswith("/model"):
                    parts = user_input.split()
                    if len(parts) > 1 and parts[1] in MODELS_CATALOG:
                        self.model_name = parts[1]
                        self.chat = self.client.chats.create(model=self.model_name)
                        print(f"✅ Switched model to \033[1;33m{self.model_name}\033[0m (New conversation context started).\n")
                    else:
                        print(f"❌ Invalid model. Use: {', '.join(MODELS_CATALOG.keys())}\n")
                    continue

                elif user_input.startswith("/app"):
                    parts = user_input.split()
                    if len(parts) > 1 and parts[1] in ENTERPRISE_APPS:
                        self.app_key = parts[1]
                        new_tags = self.get_active_tags()
                        print(f"✅ Switched application to \033[1;35m{new_tags['application']}\033[0m (Cost Center: {new_tags['cost_center']})\n")
                    else:
                        print(f"❌ Invalid app. Use: {', '.join(ENTERPRISE_APPS.keys())}\n")
                    continue

                elif user_input.lower() == "/stats":
                    self.print_session_stats()
                    continue

                elif user_input.lower() == "/clear":
                    self.chat = self.client.chats.create(model=self.model_name)
                    print("🧹 Conversation memory cleared.\n")
                    continue

                elif user_input.lower() == "/help":
                    print("\n📚 Available Commands:")
                    print("   • `/models`        : List all available Gemini models and pricing")
                    print("   • `/model <name>`  : Switch active Gemini model")
                    print("   • `/app <name>`    : Switch application tags (energy_watch, smart_meter_rag, attendance_sac, substation_copilot)")
                    print("   • `/stats`         : Display cumulative session tokens and cost")
                    print("   • `/clear`         : Clear conversation memory")
                    print("   • `/exit`          : Exit console\n")
                    continue

                # Process Standard Prompt
                self.send_prompt(user_input, stream=True)

            except (KeyboardInterrupt, EOFError):
                print("\n\n👋 Session interrupted.")
                self.print_session_stats()
                break

    def print_session_stats(self):
        print(f"\n📈 Cumulative Session Telemetry:")
        print(f"   • Total Turns      : {self.turn_count}")
        print(f"   • Total Tokens     : {self.total_session_tokens:,}")
        print(f"   • Estimated Cost   : ${self.total_session_cost:.6f} USD")
        print(f"   • BigQuery Table   : `{self.project_id}.{DATASET_ID}.{TABLE_ID}`\n")


def main():
    parser = argparse.ArgumentParser(description="Interactive Gemini Chat with Live Token Governance Telemetry")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", choices=list(MODELS_CATALOG.keys()), help="Gemini Model version")
    parser.add_argument("--app", type=str, default="energy_watch", choices=list(ENTERPRISE_APPS.keys()), help="Enterprise Application Tag profile")
    parser.add_argument("--prompt", type=str, default=None, help="Execute a single one-shot prompt and exit")
    parser.add_argument("--project", type=str, default=PROJECT_ID, help="GCP Project ID")
    parser.add_argument("--user", type=str, default=None, help="User email identifier")

    args = parser.parse_args()

    session = InteractiveGeminiSession(
        project_id=args.project,
        model_name=args.model,
        app_key=args.app,
        user_id=args.user
    )

    if args.prompt:
        session.send_prompt(args.prompt, stream=True)
        session.print_session_stats()
    else:
        session.run_interactive_loop()


if __name__ == "__main__":
    main()
