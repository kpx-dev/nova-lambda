variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "nova-lambda-fastapi-streaming-function"
}

variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "nova-lambda"
}

variable "image_tag" {
  description = "Tag of the Docker image"
  type        = string
  default     = "latest"
}