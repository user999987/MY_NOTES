```terraform
resource "aws_vpc" "main" {
  cidr_block = var.base_cidr_block
}

<BLOCK TYPE> "<BLOCK LABEL>" "<BLOCK LABEL>" {
  # Block body
  <IDENTIFIER> = <EXPRESSION> # Argument
}
```

```terraform
# Settings stay in CI/CD will override the terraform config
# If state locking fails, Terraform will not continue. You can disable state locking for most commands with the -lock flag but it is not recommended.
# To test locally if locking fails, CI/CD will be blocked
# terraform init
# terraform plan -lock=false
# Do not apply from local!

# Each Terraform module must declare which providers it requires, so that Terraform can install and use them
terraform {
  required_version = ">= 0.14.10"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.37.0"
    }
  }
# Backends define where Terraform's state snapshots are stored.
  backend "s3" {
    encrypt        = true
    bucket         = "xxx"
    key            = "xxx"
    dynamodb_table = "xxx"
    region         = "us-east-1"
  }
}

provider "aws" {
  alias  = "useast1"
  region = "us-east-1"
}

```