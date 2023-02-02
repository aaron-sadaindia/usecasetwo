resource "google_storage_bucket" "default" {
  # provider=google
  name = var.bucket_name
  storage_class = var.storage_class
  location = var.bucket_location
  lifecycle_rule {
    condition {
      age = 30
      matches_storage_class=["STANDARD"]
    }
    action {
      type = "SetStorageClass"
      storage_class="NEARLINE"
    }
  }

}