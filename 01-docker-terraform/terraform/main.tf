terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.30.0"
    }
  }
}


provider "google" {
  //if credentias is to be set via variable 
  //credentials = file(var.credentials)
  project = var.project
  region  = var.region
}

resource "google_storage_bucket" "demo-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
  //to make sure file that is not completely uplodaed even after day is deleted
}


resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = var.bq_dataset_name
}