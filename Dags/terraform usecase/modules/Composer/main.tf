resource "google_project_iam_member" "custom_service_account" {
  for_each = toset([
    "roles/composer.worker" ,
    "roles/bigquery.admin",
    "roles/storage.admin",
    "roles/compute.networks.create"
  ])
  role = each.key
  member = format("serviceAccount:%s", google_service_account.custom_service_account.email)
  project = var.project_id
  provider = google-beta
  depends_on = [
    google_service_account.custom_service_account
  ]
}


resource "google_service_account" "custom_service_account" {
  provider = google
  account_id   = "tfcomposer-service-account"
  display_name = "Cloud Composer Service Account"
}

resource "google_compute_network" "test" {
  name                    = "composer-test-network3"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "test" {
  name          = "composer-test-subnetwork"
  ip_cidr_range = "10.2.0.0/16"
  region        = "us-central1"
  network       = google_compute_network.test.id
}
resource "google_storage_bucket" "logbucketcreate" {
  name          = "composer_logs"
  location      = "US"
  force_destroy = true
}

resource "google_logging_project_sink" "instance-sink" {
  name        = "composer_logs-sink"
  description = "errors log from composer"
  destination = "storage.googleapis.com/${google_storage_bucket.logbucketcreate.name}"
  filter      = "resource.type = cloud_composer_environment AND resource.labels.instance_id = \"${var.composer_env_name}\" AND resource.labels.location=\"asia-east2\" AND severity=ERROR"

  unique_writer_identity = true
}



resource "google_composer_environment" "composer_env" {
  provider = google-beta
  project = var.project_id
  name    = var.composer_env_name
  region  = var.region
  depends_on = [
    google_project_iam_member.custom_service_account
  ]

  config {
    node_count=3
    node_config {
      service_account= google_service_account.custom_service_account.email
      disk_size_gb=30
      
    }

    software_config {
          pypi_packages            = var.pypi_packages
          env_variables            = var.env_variables
          image_version            = var.image_version
          scheduler_count=1
    }

    database_config{
        machine_type="db-n1-standard-2"
    }

    web_server_config{
        machine_type="composer-n1-webserver-2"
    }
}
}