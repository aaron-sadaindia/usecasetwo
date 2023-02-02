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