resource "google_project_iam_member" "custom_service_account" {
  for_each = toset([
    "roles/composer.worker" ,
    "roles/bigquery.admin",
    "roles/storage.admin",
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
  account_id   = "composer-service-account"
  display_name = "Cloud Composer Service Account"
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