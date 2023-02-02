variable "var_project" {
        default = "project-name"
    }
variable "env" {
        default = "dev"
    }
variable "project_id" {
  type = string
}
variable "region" {
  description = "Region where the Cloud Composer Environment is created."
  type        = string
}
variable "bucket_name" {

  type = string
  description = "The name of our bucket"
  default="sustainit2"
}
variable "bucket_location" {

  type = string
  default = "us-central1"

}


variable "storage_class" {

  type = string
  default = "STANDARD"

}


variable "composer_env_name" {
  description = "Name of Cloud Composer Environment"
  type        = string
  default="usecase-env"
}


variable "composer_service_account" {
  description = "Service Account for running Cloud Composer."
  type        = string
  default     = "null"
}



variable "env_variables" {
  type        = map(string)
  description = "Variables of the airflow environment."
  default     = {}
}

variable "image_version" {
  type        = string
  description = "The version of the aiflow running in the cloud composer environment."
  default     = "composer-1.20.0-airflow-2.3.4"
}
variable "pypi_packages" {
  description = "PyPI packages"
  type        = map(string)
  default     = {
    "openpyxl"=">=3.0.10",
  }
}