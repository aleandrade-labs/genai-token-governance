"""
Generates the official Google Cloud Mingrammer-style Architecture Diagram for GenAI Token Governance.
Features authentic Google Cloud service icons, white canvas, light gray cluster groupings,
and clear directional flow arrows.
"""
import os

def render_genai_governance_mingrammer_svg(output_path: str):
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1350 820" width="100%" height="100%" style="background-color: #ffffff; font-family: 'Google Sans', Roboto, Arial, sans-serif;">
  <defs>
    <!-- Shadows -->
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000000" flood-opacity="0.08" />
    </filter>
    <filter id="iconShadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.15" />
    </filter>

    <!-- Arrow Markers -->
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#5f6368" />
    </marker>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1a73e8" />
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#1e8e3e" />
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d93025" />
    </marker>
    <marker id="arrowYellow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#f9ab00" />
    </marker>

    <!-- ICONS -->
    <g id="icon-user">
      <rect width="64" height="64" rx="12" fill="#e8f0fe" />
      <circle cx="32" cy="24" r="10" fill="#1a73e8" />
      <path d="M 16 50 C 16 38, 48 38, 48 50 Z" fill="#1a73e8" />
    </g>

    <g id="icon-adk">
      <rect width="64" height="64" rx="12" fill="#e6f4ea" />
      <circle cx="32" cy="32" r="20" fill="#1e8e3e" />
      <rect x="22" y="24" width="20" height="16" rx="4" fill="#ffffff" />
      <circle cx="28" cy="32" r="2" fill="#1e8e3e" />
      <circle cx="36" cy="32" r="2" fill="#1e8e3e" />
      <line x1="32" y1="18" x2="32" y2="24" stroke="#ffffff" stroke-width="2" />
      <circle cx="32" cy="18" r="2" fill="#ffffff" />
    </g>

    <g id="icon-scada">
      <rect width="64" height="64" rx="12" fill="#fef7e0" />
      <polygon points="32,12 50,22 50,42 32,52 14,42 14,22" fill="#f9ab00" />
      <path d="M 32 20 L 26 32 L 34 32 L 30 44 L 40 30 L 32 30 Z" fill="#ffffff" />
    </g>

    <g id="icon-plugin">
      <rect width="64" height="64" rx="12" fill="#e8f0fe" />
      <rect x="18" y="18" width="28" height="28" rx="6" fill="#1a73e8" />
      <path d="M 26 32 L 32 38 L 42 26" stroke="#ffffff" stroke-width="3" stroke-linecap="round" fill="none" />
    </g>

    <g id="icon-vertex">
      <rect width="64" height="64" rx="12" fill="#fce8e6" />
      <circle cx="32" cy="32" r="20" fill="#d93025" />
      <circle cx="24" cy="28" r="4" fill="#ffffff" />
      <circle cx="40" cy="28" r="4" fill="#ffffff" />
      <circle cx="32" cy="42" r="4" fill="#ffffff" />
      <line x1="24" y1="28" x2="32" y2="42" stroke="#ffffff" stroke-width="2" />
      <line x1="40" y1="28" x2="32" y2="42" stroke="#ffffff" stroke-width="2" />
      <line x1="24" y1="28" x2="40" y2="28" stroke="#ffffff" stroke-width="2" />
    </g>

    <g id="icon-bigquery">
      <rect width="64" height="64" rx="12" fill="#e8f0fe" />
      <ellipse cx="32" cy="24" rx="15" ry="5" fill="#4285f4" />
      <path d="M 17 24 L 17 40 C 17 44 47 44 47 40 L 47 24" fill="#1a73e8" />
      <ellipse cx="32" cy="40" rx="15" ry="5" fill="#4285f4" />
      <circle cx="38" cy="38" r="7" fill="#ffffff" stroke="#1a73e8" stroke-width="2" />
      <line x1="43" y1="43" x2="48" y2="48" stroke="#1a73e8" stroke-width="3" stroke-linecap="round" />
    </g>

    <g id="icon-looker">
      <rect width="64" height="64" rx="12" fill="#fef7e0" />
      <rect x="18" y="34" width="7" height="16" rx="2" fill="#4285f4" />
      <rect x="29" y="24" width="7" height="26" rx="2" fill="#ea4335" />
      <rect x="40" y="16" width="7" height="34" rx="2" fill="#34a853" />
    </g>

    <g id="icon-chat">
      <rect width="64" height="64" rx="12" fill="#e6f4ea" />
      <path d="M 18 20 C 18 16 46 16 46 20 L 46 38 C 46 42 36 42 32 46 L 26 42 L 18 42 Z" fill="#1e8e3e" />
      <circle cx="26" cy="29" r="2.5" fill="#ffffff" />
      <circle cx="32" cy="29" r="2.5" fill="#ffffff" />
      <circle cx="38" cy="29" r="2.5" fill="#ffffff" />
    </g>
  </defs>

  <!-- Header -->
  <text x="50" y="50" fill="#202124" font-size="22" font-weight="700">Google Cloud FinOps — GenAI Token &amp; Cost Governance Architecture</text>
  <text x="50" y="75" fill="#5f6368" font-size="14">Official Google ADK BigQuery Agent Analytics Integration (adk.dev • Storage Write API • Zero API Keys)</text>

  <!-- Cluster 1: Authenticated Callers -->
  <rect x="50" y="110" width="220" height="660" rx="12" fill="#f8f9fa" stroke="#dadce0" stroke-width="1.5" stroke-dasharray="4,4" />
  <rect x="70" y="98" width="180" height="24" rx="6" fill="#e8eaed" />
  <text x="160" y="115" fill="#3c4043" font-size="12" font-weight="700" text-anchor="middle">1. Authenticated Callers</text>

  <g transform="translate(128, 170)" filter="url(#iconShadow)">
    <use href="#icon-user" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">Admin User</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">admin@altostrat.com</text>
  </g>

  <g transform="translate(128, 360)" filter="url(#iconShadow)">
    <use href="#icon-user" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">Enterprise Workloads</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">SAC, Grid, P&amp;D Callers</text>
  </g>

  <rect x="70" y="520" width="180" height="110" rx="8" fill="#ffffff" stroke="#dadce0" stroke-width="1" filter="url(#cardShadow)" />
  <text x="80" y="545" fill="#1a73e8" font-size="11" font-weight="700">Identity Context:</text>
  <text x="80" y="565" fill="#3c4043" font-size="10">• Google Cloud ADC Auth</text>
  <text x="80" y="583" fill="#3c4043" font-size="10">• Quota Project Enforced</text>
  <text x="80" y="601" fill="#3c4043" font-size="10">• SAP Cost Centers</text>
  <text x="80" y="619" fill="#1e8e3e" font-size="10" font-weight="700">Zero API Keys Required</text>


  <!-- Cluster 2: Google ADK Engine -->
  <rect x="320" y="110" width="310" height="660" rx="12" fill="#f8f9fa" stroke="#1e8e3e" stroke-width="1.5" stroke-dasharray="4,4" />
  <rect x="340" y="98" width="270" height="24" rx="6" fill="#e6f4ea" />
  <text x="475" y="115" fill="#1e8e3e" font-size="12" font-weight="700" text-anchor="middle">2. Google ADK Runtime Engine (adk.dev)</text>

  <g transform="translate(370, 170)" filter="url(#iconShadow)">
    <use href="#icon-adk" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">Google ADK Agent</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">smart_grid_assistant</text>
  </g>

  <g transform="translate(510, 170)" filter="url(#iconShadow)">
    <use href="#icon-scada" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">SCADA Tool</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">query_substation_status</text>
  </g>

  <g transform="translate(443, 350)" filter="url(#iconShadow)">
    <use href="#icon-plugin" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">ADK BigQuery Plugin</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">BigQueryAgentAnalyticsPlugin</text>
  </g>

  <rect x="345" y="500" width="260" height="150" rx="8" fill="#ffffff" stroke="#dadce0" stroke-width="1" filter="url(#cardShadow)" />
  <text x="360" y="525" fill="#1e8e3e" font-size="11" font-weight="700">Official ADK Capabilities:</text>
  <text x="360" y="545" fill="#3c4043" font-size="11">• Multi-Turn InMemoryRunner</text>
  <text x="360" y="565" fill="#3c4043" font-size="11">• Autonomous Tool Calling</text>
  <text x="360" y="585" fill="#3c4043" font-size="11">• gRPC Storage Write API</text>
  <text x="360" y="605" fill="#3c4043" font-size="11">• Sub-Second Streaming (&lt; 1s)</text>
  <text x="360" y="625" fill="#1a73e8" font-size="11" font-weight="700">Live Telemetry Ingestion</text>


  <!-- Cluster 3: Vertex AI Model Garden -->
  <rect x="680" y="110" width="290" height="310" rx="12" fill="#f8f9fa" stroke="#d93025" stroke-width="1.5" stroke-dasharray="4,4" />
  <rect x="700" y="98" width="250" height="24" rx="6" fill="#fce8e6" />
  <text x="825" y="115" fill="#d93025" font-size="12" font-weight="700" text-anchor="middle">3. Vertex AI Model Garden</text>

  <g transform="translate(740, 170)" filter="url(#iconShadow)">
    <use href="#icon-vertex" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">Gemini 1.5 &amp; 2.0 Flash</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">Sub-Second Dispatch</text>
  </g>

  <g transform="translate(860, 170)" filter="url(#iconShadow)">
    <use href="#icon-vertex" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">Gemini 1.5 Pro</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">Complex RAG Reasoning</text>
  </g>

  <rect x="700" y="300" width="250" height="85" rx="8" fill="#ffffff" stroke="#dadce0" stroke-width="1" filter="url(#cardShadow)" />
  <text x="715" y="325" fill="#d93025" font-size="11" font-weight="700">Token Metrics Emitted:</text>
  <text x="715" y="345" fill="#3c4043" font-size="11">• prompt_token_count (Inbound)</text>
  <text x="715" y="365" fill="#3c4043" font-size="11">• candidates_token_count (Outbound)</text>


  <!-- Cluster 4: BigQuery Analytics -->
  <rect x="680" y="460" width="290" height="310" rx="12" fill="#f8f9fa" stroke="#1a73e8" stroke-width="1.5" stroke-dasharray="4,4" />
  <rect x="700" y="448" width="250" height="24" rx="6" fill="#e8f0fe" />
  <text x="825" y="465" fill="#1a73e8" font-size="12" font-weight="700" text-anchor="middle">4. BigQuery Analytics Engine</text>

  <g transform="translate(793, 510)" filter="url(#iconShadow)">
    <use href="#icon-bigquery" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">BigQuery Telemetry</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">genai_finops_governance</text>
  </g>

  <rect x="700" y="630" width="250" height="110" rx="8" fill="#ffffff" stroke="#dadce0" stroke-width="1" filter="url(#cardShadow)" />
  <text x="715" y="655" fill="#1a73e8" font-size="11" font-weight="700">6 Pre-Calculated Analytical Views:</text>
  <text x="715" y="675" fill="#3c4043" font-size="11">• v_adk_executive_kpis</text>
  <text x="715" y="695" fill="#3c4043" font-size="11">• v_adk_user_leaderboard</text>
  <text x="715" y="715" fill="#3c4043" font-size="11">• v_adk_model_distribution</text>


  <!-- Cluster 5: Dashboards & Alerts -->
  <rect x="1020" y="110" width="280" height="660" rx="12" fill="#f8f9fa" stroke="#f9ab00" stroke-width="1.5" stroke-dasharray="4,4" />
  <rect x="1040" y="98" width="240" height="24" rx="6" fill="#fef7e0" />
  <text x="1160" y="115" fill="#b06000" font-size="12" font-weight="700" text-anchor="middle">5. Executive BI &amp; Alerting</text>

  <g transform="translate(1128, 170)" filter="url(#iconShadow)">
    <use href="#icon-looker" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">Looker Studio</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">Executive Dashboard</text>
  </g>

  <g transform="translate(1128, 360)" filter="url(#iconShadow)">
    <use href="#icon-chat" />
    <text x="32" y="80" fill="#202124" font-size="12" font-weight="700" text-anchor="middle">Google Chat Webhook</text>
    <text x="32" y="95" fill="#5f6368" font-size="11" text-anchor="middle">Budget Cards (AAQAOt)</text>
  </g>

  <rect x="1040" y="500" width="240" height="150" rx="8" fill="#ffffff" stroke="#dadce0" stroke-width="1" filter="url(#cardShadow)" />
  <text x="1055" y="525" fill="#f9ab00" font-size="11" font-weight="700">Executive Looker Metrics:</text>
  <text x="1055" y="545" fill="#3c4043" font-size="11">• Total Tokens &amp; Cost USD</text>
  <text x="1055" y="565" fill="#3c4043" font-size="11">• Top User Leaderboard Ranking</text>
  <text x="1055" y="585" fill="#3c4043" font-size="11">• Model Family Donut Share</text>
  <text x="1055" y="605" fill="#3c4043" font-size="11">• SAP Cost Center Chargeback</text>
  <text x="1055" y="625" fill="#1e8e3e" font-size="11" font-weight="700">Real-Time Refresh Enabled</text>

  <!-- ==================== FLOW ARROWS ==================== -->

  <!-- User to ADK Agent -->
  <path d="M 192 202 L 370 202" stroke="#1a73e8" stroke-width="2.5" marker-end="url(#arrowBlue)" />
  <path d="M 192 392 L 290 392 L 290 220 L 370 220" stroke="#1a73e8" stroke-width="2" marker-end="url(#arrowBlue)" />

  <!-- ADK Agent to SCADA Tool -->
  <path d="M 434 202 L 510 202" stroke="#f9ab00" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowYellow)" />

  <!-- ADK Agent to Vertex AI -->
  <path d="M 434 185 L 600 185 L 600 140 L 740 185" stroke="#d93025" stroke-width="2.5" marker-end="url(#arrowRed)" />

  <!-- ADK Agent to BigQuery Plugin -->
  <path d="M 402 245 L 402 382 L 443 382" stroke="#1e8e3e" stroke-width="3" marker-end="url(#arrowGreen)" />

  <!-- BigQuery Plugin to BigQuery Table -->
  <path d="M 507 382 L 650 382 L 650 542 L 793 542" stroke="#1a73e8" stroke-width="3" marker-end="url(#arrowBlue)" />

  <!-- BigQuery to Looker Studio -->
  <path d="M 857 542 L 1000 542 L 1000 202 L 1128 202" stroke="#f9ab00" stroke-width="2.5" marker-end="url(#arrow)" />

  <!-- BigQuery to Google Chat -->
  <path d="M 857 560 L 1000 560 L 1000 392 L 1128 392" stroke="#1e8e3e" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrowGreen)" />

</svg>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"✅ Rendered: {output_path}")

if __name__ == "__main__":
    render_genai_governance_mingrammer_svg("/Users/alexandrade/codes/catlab/light/genai-token-governance/docs/architecture_genai_governance.svg")
