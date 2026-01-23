module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"

  name = "task-telemetry-vpc"
  cidr = "10.0.0.0/16"

  # We need at least 2 zones for EKS high availability
  azs             = ["ap-south-1a", "ap-south-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true # EKS nodes need this to talk to the internet
  single_nat_gateway = true # Saves money (only creates one instead of two)

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }
}