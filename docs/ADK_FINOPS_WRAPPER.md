# 🤖 Agent Development Kit (ADK) FinOps Governance Guide

**Audience:** AI Engineers, Python Developers, Software Architects  
**Purpose:** Instructions and reference implementation for instrumenting ADK agents, multi-step reasoning loops, and Vertex AI GenerativeModel calls with **FinOps token governance metadata**.

---

## 🎯 The Challenge in Agentic Workflows

Autonomous agents built with the **Google Cloud Agent Development Kit (ADK)** introduce unique FinOps challenges:

1. **Multi-Turn Reasoning Loops**: A single user prompt may trigger 5–10 internal LLM reasoning calls as the agent thinks, invokes tools, analyzes results, and refines answers.
2. **Exponential Context Growth**: If intermediate tool outputs (e.g. large SQL tables or documents) are appended to conversation history without truncation, prompt token consumption grows exponentially with each step.
3. **Attribution Blindspots**: Calls made by backend services or Cloud Functions typically use a single Service Account, obscuring which end-user or business department initiated the action.

---

## 🛠️ The Solution: The ADK FinOps Metadata Wrapper

The `FinOpsGenerativeModel` interceptor automatically:
- Injects customer policy tags (`cost_center`, `app_code`, `environment`, `user_id`) into every request.
- Logs exact prompt tokens, candidate output tokens, and cached tokens per turn.
- Emits structured JSON logs ingested into BigQuery in real time.

### 📋 Complete Python Implementation:

```python
import json
import logging
import time
from typing import Optional, Dict, Any, List
import google.cloud.logging
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationResponse, Content, Tool

# Initialize GCP Cloud Logging
try:
    log_client = google.cloud.logging.Client()
    log_client.setup_logging()
except Exception:
    pass

logger = logging.getLogger("finops_ai_governance")

class FinOpsGenerativeModel:
    """
    Production wrapper for Vertex AI GenerativeModel and ADK Agent workflows.
    Ensures complete telemetry attribution for user, application, and SAP cost center.
    """
    def __init__(
        self,
        model_name: str,
        app_code: str,
        cost_center: str,
        user_id: str,
        agent_name: Optional[str] = "default_agent",
        environment: str = "prod",
        project_id: Optional[str] = None,
        location: str = "us-central1"
    ):
        self.model_name = model_name
        self.app_code = app_code
        self.cost_center = cost_center
        self.user_id = user_id
        self.agent_name = agent_name
        self.environment = environment
        self.project_id = project_id or vertexai.preview.initializer.global_config.project
        
        # Initialize underlying Vertex AI Model
        self.model = GenerativeModel(model_name)

    def generate_content(
        self,
        contents: Any,
        session_id: Optional[str] = "session_default",
        turn_number: int = 1,
        tools: Optional[List[Tool]] = None,
        tool_name_invoked: Optional[str] = None,
        **kwargs
    ) -> GenerationResponse:
        """
        Executes model generation and streams FinOps token metrics to Cloud Logging / BigQuery.
        """
        start_time = time.time()
        
        # 1. Execute Vertex AI Call
        response = self.model.generate_content(contents, tools=tools, **kwargs)
        latency_ms = round((time.time() - start_time) * 1000, 2)

        # 2. Extract Token Usage Metadata
        usage = response.usage_metadata
        prompt_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        total_tokens = usage.total_token_count or 0
        cached_tokens = getattr(usage, "cached_content_token_count", 0) or 0

        # 3. Emit Structured FinOps Telemetry Log
        telemetry_record = {
            "event_type": "vertex_ai_generation",
            "model": self.model_name,
            "project_id": self.project_id,
            "session_id": session_id,
            "turn_number": turn_number,
            "agent_name": self.agent_name,
            "tool_invoked": tool_name_invoked or "none",
            "latency_ms": latency_ms,
            "usageMetadata": {
                "promptTokenCount": prompt_tokens,
                "candidatesTokenCount": output_tokens,
                "cachedContentTokenCount": cached_tokens,
                "totalTokenCount": total_tokens
            },
            "customLabels": {
                "user": self.user_id,
                "app_code": self.app_code,
                "cost_center": self.cost_center,
                "environment": self.environment
            }
        }

        # Log as structured JSON (Cloud Logging Router streams directly to BigQuery)
        logger.info(json.dumps(telemetry_record))

        return response
```

---

## 🚀 Example Usage in an ADK Application

```python
# 1. Instantiate instrumented model
agent_llm = FinOpsGenerativeModel(
    model_name="gemini-1.5-flash",
    app_code="cds-34199",
    cost_center="18207243",
    user_id="raphael_cano",
    agent_name="smart_reader_analyst"
)

# 2. Execute multi-turn request
response = agent_llm.generate_content(
    contents="Identify high-consumption outliers in substation feeder 4.",
    session_id="session_user_891274",
    turn_number=1
)

print(response.text)
```

---

## 📈 Optimization Best Practices for ADK Agents

1. **Enable Context Caching**: For system instructions or large domain documents repeated across multi-turn sessions, use Vertex AI Context Caching to save **up to 75%** on prompt tokens.
2. **Truncate Tool Outputs**: Cap database or search result lengths before appending to agent message history.
3. **Use Flash as Reasoning Engine**: Route 80%+ of reasoning tasks to `gemini-1.5-flash` and escalate to `gemini-1.5-pro` only for complex multi-modal synthesis.
