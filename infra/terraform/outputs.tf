output "instance_public_ip" {
  description = "EC2 public IP of InfraTrack"
  value       = aws_instance.web.public_ip
}

output "instance_public_dns" {
  description = "Public DNS of the EC2 instance"
  value       = aws_instance.web.public_dns
}

output "security_group_id" {
  description = "SG ID attached to the EC2 instance"
  value       = aws_security_group.web_sg.id
}

output "ec2_role_arn" {
  description = "IAM Role ARN attached to the EC2 instance"
  value       = aws_iam_role.ec2_role.arn
}

output "instance_profile_name" {
  description = "Instance profile name attached to the EC2 instance"
  value       = aws_iam_instance_profile.ec2_profile.name
}

