provider "google" {

  project = var.project_id
  region  = var.region
  credentials = file("/Users/aaron.john/Downloads/sadaindia-tvm-poc-de-ea611cb2648c.json")

}
provider "google-beta" {

    credentials = file("/Users/aaron.john/Downloads/sadaindia-tvm-poc-de-ea611cb2648c.json")

}