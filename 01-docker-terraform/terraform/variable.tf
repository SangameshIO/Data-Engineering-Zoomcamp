variable "credentials" {
  description = "GCP credentials in JSON format"
  default     = "./credentials.json"
}


variable "location" {
  description = "The location of the resources"
  default     = "US"
}

variable "region" {
  description = "region"
  default     = "us-central1"
}
variable "project" {
  description = "GCP project ID"
  default     = "terraform-495116"
}


variable "bq_dataset_name" {
  description = "My big query dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-495116-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage class"
  default     = "STANDARD"
}