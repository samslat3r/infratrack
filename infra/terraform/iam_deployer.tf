terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = ">= 5.0" }
  }
}

provider "aws" {
  region = var.region
}

# Deployer role & permission boundary
data "aws_caller_identity" "me" {}

# Permission Boundary. (EKS/Lambda listed for flexibility ; not necessarily used currently)
resource "aws_iam_policy" "boundary" {
  name   = "${var.prefix}-boundary"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "iam:AttachRolePolicy","iam:PutRolePolicy","iam:CreateRole","iam:DeleteRole","iam:TagRole",
          "iam:CreateInstanceProfile","iam:AddRoleToInstanceProfile",
          "iam:RemoveRoleFromInstanceProfile","iam:DeleteInstanceProfile"
        ],
        Resource = [
          "arn:aws:iam::${data.aws_caller_identity.me.account_id}:role/${var.prefix}-*",
          "arn:aws:iam::${data.aws_caller_identity.me.account_id}:instance-profile/${var.prefix}-*"
        ]
      },
      {
        Effect   = "Allow",
        Action   = ["iam:PassRole"],
        Resource = "arn:aws:iam::${data.aws_caller_identity.me.account_id}:role/${var.prefix}-*",
        Condition = {
          StringEqualsIfExists = {
            "iam:PassedToService" = [
              "ec2.amazonaws.com",
              "ecs.amazonaws.com",
              "ecs-tasks.amazonaws.com",
              "eks.amazonaws.com",
              "lambda.amazonaws.com"
            ]
          }
        }
      }
    ]
  })
}

# Deployer Policy
resource "aws_iam_policy" "deployer" {
  name   = "${var.prefix}-deployer-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      { Effect = "Allow", Action = ["sts:GetCallerIdentity"], Resource = "*" },
      { Effect = "Allow", Action = ["ec2:*"], Resource = "*" },
      {
        Effect = "Allow",
        Action = [
          "iam:CreateRole","iam:DeleteRole","iam:GetRole","iam:TagRole",
          "iam:AttachRolePolicy","iam:DetachRolePolicy","iam:PutRolePolicy","iam:DeleteRolePolicy",
          "iam:CreateInstanceProfile","iam:DeleteInstanceProfile",
          "iam:AddRoleToInstanceProfile","iam:RemoveRoleFromInstanceProfile",
          "iam:ListAttachedRolePolicies","iam:ListRolePolicies",
          "iam:ListInstanceProfilesForRole","iam:ListRoles","iam:GetInstanceProfile"
        ],
        Resource = [
          "arn:aws:iam::${data.aws_caller_identity.me.account_id}:role/${var.prefix}-*",
          "arn:aws:iam::${data.aws_caller_identity.me.account_id}:instance-profile/${var.prefix}-*"
        ]
      },
      {
        Effect   = "Allow",
        Action   = ["iam:PassRole"],
        Resource = "arn:aws:iam::${data.aws_caller_identity.me.account_id}:role/${var.prefix}-*",
        Condition = {
          StringEqualsIfExists = {
            "iam:PassedToService" = [
              "ec2.amazonaws.com","ecs.amazonaws.com","ecs-tasks.amazonaws.com",
              "eks.amazonaws.com","lambda.amazonaws.com"
            ]
          }
        }
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents","logs:Describe*",
          "ssm:Describe*","ssm:Get*","ssm:List*","ec2messages:*","ssmmessages:*",
          "s3:ListBucket","s3:GetObject","s3:PutObject"
        ],
        Resource = "*"
      }
    ]
  })
}

# Deployer Role 
resource "aws_iam_role" "deployer_role" {
  name = "${var.prefix}-deployer-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { AWS = var.deployer_principals },
      Action    = "sts:AssumeRole",
      Condition = { Bool = { "aws:MultiFactorAuthPresent" = "true" } }
    }]
  })

  # Permission boundary keeps this role constrained to infratrack-* resources
  permissions_boundary = aws_iam_policy.boundary.arn
}

resource "aws_iam_role_policy_attachment" "attach_deployer" {
  role       = aws_iam_role.deployer_role.name
  policy_arn = aws_iam_policy.deployer.arn
}

