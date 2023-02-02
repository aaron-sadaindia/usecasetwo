terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.44.1"
    }
  }
}

module "gcs_bucket" {
  source = "/Users/aaron.john/Desktop/Composer/Dags/terraform usecase/modules/gcs_bucket"
  bucket_name=var.bucket_name
  bucket_location=var.bucket_location
  storage_class=var.storage_class
}
module "Big_query" {
    source= "/Users/aaron.john/Desktop/Composer/Dags/terraform usecase/modules/Big_query"
    project_id=var.project_id
    region=var.region 
    
}
module "Composer" {
  source  = "/Users/aaron.john/Desktop/Composer/Dags/terraform usecase/modules/Composer"
  project_id=var.project_id
  region=var.region
  composer_env_name=var.composer_env_name
  composer_service_account=var.composer_service_account
  env_variables=var.env_variables
  image_version=var.image_version
  pypi_packages=var.pypi_packages
}