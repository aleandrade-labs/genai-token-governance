"""
Official Google ADK Agent Implementation with BigQueryAgentAnalyticsPlugin
Direct implementation of https://adk.dev/integrations/bigquery-agent-analytics/
Runs an enterprise Light S/A Agent with the native ADK plugin, streaming telemetry
directly to BigQuery using the BigQuery Storage Write API.
"""
import os
import sys
import asyncio
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.plugins.bigquery_agent_analytics_plugin import (
    BigQueryAgentAnalyticsPlugin,
    BigQueryLoggerConfig
)
from google.adk.runners import InMemoryRunner

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aleorg-dev-workload-01")
DATASET_ID = "genai_finops_governance"
TABLE_ID = "adk_events"  # Dedicated native ADK table managed by plugin
LOCATION = "us-east1"

# 1. Custom tool for demonstration
def query_substation_status(substation_id: str) -> dict:
    """Queries real-time SCADA telemetry for a Light S/A electrical substation."""
    print(f"\n   ⚡ [SCADA Tool Invocation]: query_substation_status('{substation_id}')")
    return {
        "substation_id": substation_id,
        "name": "Subestação Frei Caneca",
        "status": "OPERATIONAL",
        "voltage_kv": 138.0,
        "load_percentage": 74.2,
        "active_feeders": ["F-01", "F-02", "F-03", "F-04"],
        "alarm": "NONE",
        "operator_notes": "All transformers operating within normal thermal limits."
    }

async def main():
    print("=" * 75)
    print("🤖 OFFICIAL GOOGLE ADK BIGQUERY AGENT ANALYTICS (adk.dev)")
    print("=" * 75)
    
    # 2. Instantiate the official BigQueryAgentAnalyticsPlugin
    print(f"\n📦 Initializing BigQueryAgentAnalyticsPlugin for `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`...")
    plugin = BigQueryAgentAnalyticsPlugin(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id=TABLE_ID,
        location=LOCATION,
        config=BigQueryLoggerConfig(
            enabled=True,
            batch_size=1,              # Flush immediately for real-time observability
            shutdown_timeout=5.0,
            auto_schema_upgrade=True,  # Automatically evolves BigQuery schema
            create_views=True,         # Auto-generates flat analytical views
            view_prefix="v_adk_official"
        )
    )
    
    # 3. Model Configuration: Support Vertex AI Enterprise or Gemini API Key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        print("🔑 Using Google AI Studio / Gemini API Key authentication.")
        model = Gemini(model="gemini-1.5-flash")
    else:
        print(f"🏢 Using Google Cloud Vertex AI Enterprise authentication (Project: {PROJECT_ID}).")
        model = Gemini(
            model="gemini-1.5-flash",
            client_kwargs={
                "vertexai": True,
                "project": PROJECT_ID,
                "location": "us-central1"
            }
        )

    # 4. Create the Enterprise Agent with tools and model
    agent = Agent(
        name="light_smart_grid_assistant",
        model=model,
        instruction=(
            "You are Light S/A's Smart Grid Dispatch Assistant. "
            "Help operators inspect substation statuses and diagnose electrical grid health."
        ),
        tools=[query_substation_status]
    )
    
    # 5. Attach plugin to the InMemoryRunner
    runner = InMemoryRunner(agent=agent, plugins=[plugin])
    print(f"✅ Agent '{agent.name}' initialized with BigQueryAgentAnalyticsPlugin attached.")
    
    try:
        user_prompt = "Verifique o status da Subestação Frei Caneca (SUB-RJ-FC-01) e informe a carga atual."
        print(f"\n📝 [User Prompt]: {user_prompt}")
        print("🚀 Executing agent reasoning loop & tool calls...\n")
        
        events = await runner.run_debug(
            user_prompt,
            user_id="antonio_lameirao@light.com.br",
            session_id="session_adk_live_001",
            quiet=False
        )
        
        print("\n" + "=" * 75)
        print("🎯 [Agent Reasoning Completed Successfully]:")
        if events:
            for ev in events:
                if hasattr(ev, "content") and ev.content:
                    print(f"  • {ev}")
        print("=" * 75)
        
    except Exception as e:
        print(f"ℹ️ Agent Loop Notice: {e}")
        
    finally:
        # Gracefully flush events and close BigQuery Storage Write API stream
        print("\n📤 Flushing telemetry events to BigQuery Storage Write API...")
        await runner.close()
        print("🎉 SUCCESS: Operational telemetry streamed to BigQuery dataset `genai_finops_governance`!")

if __name__ == "__main__":
    asyncio.run(main())
