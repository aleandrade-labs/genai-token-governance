output "bigquery_dataset_id" {
  description = "The BigQuery dataset created for GenAI token telemetry"
  value       = google_bigquery_dataset.genai_dataset.dataset_id
}

output "log_sink_name" {
  description = "Name of the Cloud Logging sink routing AI telemetry to BigQuery"
  value       = google_logging_project_sink.vertex_telemetry_sink.name
}

output "log_sink_writer_identity" {
  description = "Service account of the Cloud Logging sink"
  value       = google_logging_project_sink.vertex_telemetry_sink.writer_identity
}
