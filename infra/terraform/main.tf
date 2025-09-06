# Core infrastructure: EC2, SG, Instance Profile

# Default VPC - simple networking for prototype/mvp
data "aws_vpc" "default" {
  default = true
}

# Ubuntu 24.04 (Noble) x86_64 HVM EBS — Canonical
data "aws_ami" "ubuntu_2404" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    # Note the leading wildcard after ubuntu/images/
    values = ["ubuntu/images/*ubuntu-noble-24.04-amd64-server-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# Import local key pair
resource "aws_key_pair" "deploy_key" {
  key_name   = var.key_name
  public_key = file(var.public_key_path)
}

# SG Allows HTTP and SSH
resource "aws_security_group" "web_sg" {
  name        = "${var.prefix}-sg"
  description = "Allow HTTP (80) and SSH (22)"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all egress"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.prefix}-sg"
  }
}

# EC2 Instance Role + Instance Profile (with infratrack-* boundary)
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    sid     = "EC2AssumeRole"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ec2_role" {
  name               = "${var.prefix}-ec2-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json

  tags = {
    Name = "${var.prefix}-ec2-role"
  }
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "${var.prefix}-instance-profile"
  role = aws_iam_role.ec2_role.name
}


# EC2 Instance


resource "aws_instance" "web" {
  ami                         = data.aws_ami.ubuntu_2404.id
  instance_type               = var.instance_type
  key_name                    = aws_key_pair.deploy_key.key_name
  iam_instance_profile        = aws_iam_instance_profile.ec2_profile.name
  vpc_security_group_ids      = [aws_security_group.web_sg.id]
  associate_public_ip_address = true

  # Tweak root volume (optional)
  root_block_device {
    volume_size = 16
    volume_type = "gp3"
  }

  tags = {
    Name = "${var.prefix}-web"
  }
}

