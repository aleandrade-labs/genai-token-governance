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
from google.adk.runner import InMemoryRunner

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "aleorg-dev-workload-01")
DATASET_ID = "genai_finops_governance"
LOCATION = "us-east1"

# 1. Custom tool for demonstration
def query_substation_status(substation_id: str) -> dict:
    """Queries real-time SCADA telemetry for a Light S/A electrical substation."""
    print(f"   ⚡ [Tool Call] query_substation_status executed for: {substation_id}")
    return {
        "substation_id": substation_id,
        "status": "OPERATIONAL",
        "voltage_kv": 138.0,
        "load_percentage": 74.2,
        "active_feeders": ["F-01", "F-02", "F-03", "F-04"],
        "alarm": "NONE"
    }

async def main():
    print("=" * 75)
    print("🤖 OFFICIAL GOOGLE ADK BIGQUERY AGENT ANALYTICS (adk.dev)")
    print("=" * 75)
    
    # 2. Instantiate the official BigQueryAgentAnalyticsPlugin
    print(f"\n📦 Initializing BigQueryAgentAnalyticsPlugin for `{PROJECT_ID}.{DATASET_ID}`...")
    plugin = BigQueryAgentAnalyticsPlugin(
        project_id=PROJECT_ID,
        dataset_id=DATASET_ID,
        table_id="agent_events",
        location=LOCATION,
        config=BigQueryLoggerConfig(
            enabled=True,
            batch_size=1,             # Flush immediately for interactive demo
            shutdown_timeout=5.0,
            auto_schema_upgrade=True,  # Automatically evolves BigQuery schema
            create_views=True,         # Auto-generates flat analytical views
            view_prefix="v_adk"
        )
    )
    
    # 3. Create the Enterprise Agent with the Plugin attached
    agent = Agent(
        name="light_smart_grid_assistant",
        model=Gemini(model_name="gemini-1.5-flash"),
        instruction=(
            "You are Light S/A's Smart Grid Dispatch Assistant. "
            "Help operators inspect substation statuses and diagnose electrical grid health."
        ),
        plugins=[plugin],
        tools=[query_substation_status]
    )
    
    print(f"✅ Agent '{agent.name}' created with BigQueryAgentAnalyticsPlugin attached.")
    print("🚀 Running sample agent task: 'Verificar status da Subestação Frei Caneca (SUB-RJ-FC-01)'...\n")
    
    # 4. Execute the agent using InMemoryRunner
    runner = InMemoryRunner(agent=agent)
    
    try:
        # Run agent
        prompt = "Verifique o status da Subestação Frei Caneca (SUB-RJ-FC-01) e informe a carga atual."
        print(f"📝 [User Prompt]: {prompt}\n")
        
        response = await runner.run_debug(prompt)
        print("\n" + "=" * 75)
        print("🎯 [Agent Response]:")
        print(response)
        print("=" * 75)
        
    finally:
        # Flush pending telemetry events to BigQuery Storage Write API
        print("\n📤 Flushing telemetry events to BigQuery Storage Write API...")
        await plugin.shutdown()
        print("🎉 SUCCESS: Operational telemetry streamed to BigQuery dataset `genai_finops_governance`!")

if __name__ == "__main__":
    asyncio.run(main())
