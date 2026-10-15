variable "aws_region" {
  description = "AWS region to create the infrastructure in."
  type        = string
  default     = "ap-south-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster."
  type        = string
  default     = "tutorslot-eks"
}

variable "environment" {
  description = "Environment tag applied to resources."
  type        = string
  default     = "dev"
}
