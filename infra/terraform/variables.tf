variable "region" {
  description = "AWS region to deploy into."
  type        = string
  default     = "us-west-2"
}

variable "prefix" {
  description = "Name prefix for created resources."
  type        = string
  default     = "infratrack"
}

variable "deployer_principals" {
  description = "List of AWS principals (ARNs) allowed to assume the deployer role."
  type        = list(string)
  default     = ["arn:aws:iam::9999999:user/username"] # e.g., ["arn:aws:iam::99999999:user/sam"]
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.micro"
}

variable "key_name" {
  description = "AWS Keypair name."
  type        = string
  default     = "infratrack-key"
}

variable "public_key_path" {
  description = "Local public SSH key  to create keypair."
  type        = string
  default     = "~/.ssh/infratrack.pub"
}
