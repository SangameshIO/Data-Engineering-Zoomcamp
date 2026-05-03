terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.30.0"
    }
  }
}


provider "google" {
  project = "terraform-495116"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-495116-terra-bucket"
  location      = "US"
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