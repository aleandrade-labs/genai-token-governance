variable "project_id" {
  type        = string
  description = "Google Cloud host project ID for GenAI telemetry"
  default     = "aleorg-dev-workload-01"
}

variable "region" {
  type        = string
  description = "GCP Region for BigQuery dataset"
  default     = "us-east1"
}

variable "bigquery_dataset_id" {
  type        = string
  description = "BigQuery dataset ID for GenAI telemetry"
  default     = "genai_finops_governance"
}
