provider "google" {
  project = "sample-311412"
  region  = "us-central1"
  credentials = file("credentials.json")
}

data "google_container_engine_versions" "gke_version" {
  location = "us-central1"
  version_prefix = "1.27.8-gke.1067004"
}

resource "google_container_cluster" "primary" {
    name     = "cluster-1"
    location = "us-central1"

  # We can't create a cluster with no node pool defined, but we want to only use
  # separately managed node pools. So we create the smallest possible default
  # node pool and immediately delete it.
    remove_default_node_pool = true
    initial_node_count       = 1

    network    = "default"
    subnetwork = "default"
}

# Separately Managed Node Pool
resource "google_container_node_pool" "primary_nodes" {
  name       = google_container_cluster.primary.name
  location   = "us-central1"
  cluster    = google_container_cluster.primary.name
  
  version = data.google_container_engine_versions.gke_version.release_channel_latest_version["STABLE"]
  node_count = 1

  node_config {
    oauth_scopes = [
        "https://www.googleapis.com/auth/devstorage.read_only",
        "https://www.googleapis.com/auth/logging.write",
        "https://www.googleapis.com/auth/monitoring",
        "https://www.googleapis.com/auth/servicecontrol",
        "https://www.googleapis.com/auth/service.management.readonly",
        "https://www.googleapis.com/auth/trace.append",
        "https://www.googleapis.com/auth/cloud-platform"
    ]

    labels = {
      env = "sample-311412"
    }

    # preemptible  = true
    preemptible               = false
    machine_type              = "e2-micro"
    disk_size_gb              = 10
    disk_type                 = "pd-standard"
    image_type                = "COS_CONTAINERD"
    service_account           = "default"
    shielded_instance_config {
        enable_secure_boot = true
    }
  }
}
