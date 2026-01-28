End-to-End DevSecOps Telemetry Stack 🚀
This repository contains a full-lifecycle deployment of a Flask + Redis telemetry API on AWS EKS, managed via Terraform and synchronized through GitOps.

🏗️ Architecture & Tech Stack
Cloud Provider: AWS (Region: ap-south-1)

Infrastructure as Code: Terraform (VPC, EKS, Subnets, NAT Gateways)

Orchestration: Kubernetes (AWS EKS) using t3.medium managed node groups

GitOps: ArgoCD for automated CD and drift detection

CI Pipeline: GitHub Actions for automated Docker builds and ECR pushes

Security: Trivy for container image and manifest vulnerability scanning

Observability: Prometheus & Grafana (via Helm) for real-time metrics and alerting

🛠️ Infrastructure Management

1. Provisioning:

cd terraform
terraform init
terraform apply --auto-approve

2. Cluster Connection

aws eks update-kubeconfig --region ap-south-1 --name task-telemetry-cluster

3. Security & DevSecOps: 

The CI pipeline integrates Trivy to scan the Flask application image. No high/critical vulnerabilities are permitted in the ECR registry.

4. Observability & Monitoring:

 • Metrics: Scraping application telemetry via Prometheus.

 • Alerting: Custom PrometheusRule (flask-api-alerts) injected via ArgoCD.

 • Visualization: Grafana dashboards showing pod-level CPU, Memory, and Network I/O.

5. Cleanup To avoid unnecessary AWS costs:

terraform destroy --auto-approve