"""
ADK FinOps Metadata Wrapper
Instruments Google Cloud Vertex AI & ADK Agentic calls with caller attribution,
customer policy tags (cost_center, app_code, user_id), and token-level telemetry.
"""
import json
import logging
import time
from typing import Optional, Dict, Any, List
import google.cloud.logging
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationResponse, Tool

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
        self.project_id = project_id
        
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
        prompt_tokens = getattr(usage, "prompt_token_count", 0) or 0
        output_tokens = getattr(usage, "candidates_token_count", 0) or 0
        total_tokens = getattr(usage, "total_token_count", 0) or 0
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
