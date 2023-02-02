variable "project_id" {
  description = "Project ID where Cloud Composer Environment is created."
  type        = string
  default     = "sadaindia-tvm-poc-de"
}

variable "composer_env_name" {
  description = "Name of Cloud Composer Environment"
  type        = string
  default="usecase-env"
}

variable "region" {
  description = "Region where the Cloud Composer Environment is created."
  type        = string
  default     = "us-central1"
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