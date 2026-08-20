terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Enable Required GCP APIs for GenAI Telemetry
resource "google_project_service" "services" {
  for_each = toset([
    "aiplatform.googleapis.com",
    "discoveryengine.googleapis.com",
    "bigquery.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com"
  ])
  project            = var.project_id
  service            = each.key
  disable_on_destroy = false
}

# 2. BigQuery Dataset for GenAI Telemetry & Token Analytics
resource "google_bigquery_dataset" "genai_dataset" {
  dataset_id                 = var.bigquery_dataset_id
  project                    = var.project_id
  friendly_name              = "GenAI Token & Cost Governance"
  description                = "Stores real-time token telemetry for Vertex AI, Search, and ADK"
  location                   = var.region
  delete_contents_on_destroy = false

  labels = {
    governance = "finops"
    workload   = "genai-telemetry"
  }

  depends_on = [google_project_service.services]
}

# 3. Cloud Logging Log Router Sink (Vertex AI Telemetry to BigQuery)
resource "google_logging_project_sink" "vertex_telemetry_sink" {
  name        = "vertex-ai-telemetry-sink"
  project     = var.project_id
  destination = "bigquery.googleapis.com/projects/${var.project_id}/datasets/${google_bigquery_dataset.genai_dataset.dataset_id}"

  # Captures both Vertex AI Endpoint usage metadata and application ADK telemetry
  filter = "jsonPayload.usageMetadata.totalTokenCount > 0 OR jsonPayload.event_type = \"vertex_ai_generation\" OR resource.type = \"discoveryengine.googleapis.com/DataStore\""

  unique_writer_identity = true

  bigquery_options {
    use_partitioned_tables = true
  }

  depends_on = [google_bigquery_dataset.genai_dataset]
}

# 4. Grant BigQuery Data Editor to Log Router Sink
resource "google_project_iam_member" "sink_bq_writer" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = google_logging_project_sink.vertex_telemetry_sink.writer_identity
}
