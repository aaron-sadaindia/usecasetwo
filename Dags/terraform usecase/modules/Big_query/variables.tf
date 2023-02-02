

variable "project_id" {
  type = string
  default="sadaindia-tvm-poc-de"
}
variable "region" {
  description = "Region where the Cloud Composer Environment is created."
  type        = string
  default     = "us-central1"
}