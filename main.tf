provider "google" {
  project = "crack-audio-456014-k5"
  region  = "us-central1"
}

resource "google_firestore_database" "database" {
  project     = "URL-shortener"
  name        = "(default)"
  location_id = "nam5"
  type        = "FIRESTORE_NATIVE"
}

resource "google_cloud_run_service" "url_shortener" {
  name     = "url-shortener"
  location = "us-central1"
  
  template {
    spec {
      containers {
        image = "gcr.io/crack-audio-456014-k5/url-shortener:latest"
      }
    }
  }
}

resource "google_project_iam_member" "run_invoker" {
  project = "crack-audio-456014-k5"
  role    = "roles/run.invoker"
  member  = "allUsers"
}
