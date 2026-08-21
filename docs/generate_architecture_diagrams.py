"""
Python script using mingrammer/diagrams to generate official Google Cloud Architecture diagrams.
"""
import os
import sys

# Ensure dot is in PATH
os.environ["PATH"] = "/opt/homebrew/Cellar/graphviz/15.1.1/bin:/opt/homebrew/bin:" + os.environ.get("PATH", "")

from diagrams import Diagram, Cluster, Edge
from diagrams.gcp.analytics import BigQuery, PubSub, Looker
from diagrams.gcp.compute import Functions, Run, ComputeEngine
from diagrams.gcp.ml import VertexAI
from diagrams.gcp.storage import Storage
from diagrams.gcp.operations import Monitoring, Logging
from diagrams.gcp.devtools import Scheduler
from diagrams.onprem.client import User, Users
from diagrams.saas.chat import Slack

def generate_genai_governance_diagram():
    print("🎨 Generating GenAI Token Governance Architecture Diagram...")
    out_path = "docs/architecture_genai_governance"
    
    with Diagram(
        "Google Cloud FinOps — GenAI Token & Cost Governance Architecture",
        filename=out_path,
        show=False,
        direction="TB"
    ):
        with Cluster("1. Authenticated Callers & Enterprise Users"):
            altostrat_user = User("Admin User\n(admin@altostrat.com)")
            org_users = Users("Enterprise Teams\n(SAC, Grid, P&D, SCADA)")
            
        with Cluster("2. Google Agent Development Kit (ADK Runtime)"):
            adk_agent = Functions("Google ADK Agent\n(smart_grid_assistant)")
            scada_tool = ComputeEngine("SCADA Telemetry Tool\n(query_substation_status)")
            adk_plugin = Run("BigQueryAgentAnalyticsPlugin\n(gRPC Storage Write API)")

        with Cluster("3. Google Cloud Vertex AI Model Garden"):
            gemini_flash = VertexAI("Gemini 1.5 & 2.0 Flash\n(Fast Inference)")
            gemini_pro = VertexAI("Gemini 1.5 Pro\n(Complex Reasoning)")

        with Cluster("4. Google Cloud BigQuery Telemetry Engine"):
            bq_table = BigQuery("Partitioned Raw Events\n(adk_events & agent_events)")
            with Cluster("Pre-Calculated Analytical SQL Views"):
                bq_kpis = BigQuery("v_adk_executive_kpis\n(Tokens, Latency, Cost)")
                bq_leaderboard = BigQuery("v_adk_user_leaderboard\n(Caller Ranking & SAP)")
                bq_models = BigQuery("v_adk_model_distribution\n(Family Breakdown)")

        with Cluster("5. Executive Dashboards & Alerting"):
            looker_dash = Looker("Looker Studio Dashboard\n(Real-Time Executive BI)")
            chat_alert = Slack("Chat / Webhook Channel\n(Proactive Budget Alerts)")

        # Data Flows
        altostrat_user >> Edge(color="#4285F4", label="1. Prompt Request") >> adk_agent
        org_users >> Edge(color="#4285F4") >> adk_agent
        
        adk_agent >> Edge(color="#EA4335", label="2. Model Inference", style="bold") >> gemini_flash
        adk_agent >> Edge(color="#EA4335", style="bold") >> gemini_pro
        
        adk_agent >> Edge(color="#FBBC04", label="3. Autonomous Tool Call", style="dashed") >> scada_tool
        scada_tool >> Edge(color="#FBBC04", label="Telemetry Response", style="dashed") >> adk_agent
        
        adk_agent >> Edge(color="#34A853", label="4. Telemetry Hook", style="bold") >> adk_plugin
        adk_plugin >> Edge(color="#34A853", label="5. Sub-Second Stream (<1s)", style="bold") >> bq_table
        
        bq_table >> bq_kpis
        bq_table >> bq_leaderboard
        bq_table >> bq_models
        
        bq_kpis >> Edge(color="#4285F4", label="6. Instant Visual BI") >> looker_dash
        bq_leaderboard >> Edge(color="#4285F4") >> looker_dash
        bq_models >> Edge(color="#4285F4") >> looker_dash
        
        bq_kpis >> Edge(color="#EA4335", style="dashed") >> chat_alert

    print(f"✅ Generated: {out_path}.png")

if __name__ == "__main__":
    generate_genai_governance_diagram()
