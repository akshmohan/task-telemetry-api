# 1. Define the Redis Deployment
resource "kubernetes_deployment" "redis" {
  metadata {
    name = "redis-deployment"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "redis"
      }
    }

    template {
      metadata {
        labels = {
          app = "redis"
        }
      }

      spec {
        container {
          name  = "redis"
          image = "redis:alpine"
          port {
            container_port = 6379
          }
        }
      }
    }
  }
}

# 2. Define the Redis Service
resource "kubernetes_service" "redis" {
  metadata {
    name = "redis-service"
  }
  spec {
    selector = {
      app = "redis"
    }
    port {
      port        = 6379
      target_port = 6379
    }
    type = "ClusterIP"
  }
}

# 3. Define the Flask API Deployment
resource "kubernetes_deployment" "flask_api" {
  metadata {
    name = "flask-deployment"
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "flask-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "flask-api"
        }
      }

      spec {
        container {
          name  = "flask-container"
          # Ensure this matches the tag you use in deploy.py
          image = "flask-telemetry:latest"
          image_pull_policy = "Never" # Essential for local Kind clusters

          port {
            name = "http-metrics"
            container_port = 5000
          }

          env {
            name  = "REDIS_HOST"
            value = "redis-service"
          }
        }
      }
    }
  }
}

# 4. Define the Flask API Service
resource "kubernetes_service" "flask_api" {
  metadata {
    name = "flask-service"
  }
  spec {
    selector = {
      app = "flask-api"
    }
    port {
      port        = 5000
      target_port = 5000
      node_port   = 30001
    }
    type = "NodePort"
  }
}

# 5. Deploy Prometheus Stack using Helm
resource "helm_release" "prometheus" {
  name       = "prometheus"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
  namespace  = "default"

  # We can customize values directly in HCL
  set {
    name  = "grafana.service.type"
    value = "NodePort"
  }

  set {
    name  = "grafana.service.nodePort"
    value = "30002"
  }
}

# 6. The "Bridge": Connecting Flask Metrics to Prometheus
resource "kubernetes_manifest" "flask_servicemonitor" {
  manifest = {
    apiVersion = "monitoring.coreos.com/v1"
    kind       = "ServiceMonitor"
    metadata = {
      name      = "flask-servicemonitor"
      namespace = "default"
      labels = {
        # This label MUST match the name of your Helm release from step #5
        release = "prometheus" 
      }
    }
    spec = {
      selector = {
        matchLabels = {
          app = "flask-api"
        }
      }

    endpoints = [
  {
    port = "http-metrics"
    path = "/metrics"
  }
]
    }
  }
}

# 7. Define the S3 Bucket in Localstack
resource "aws_s3_bucket" "task_storage" {
  bucket = "task-telemetry-storage"
}