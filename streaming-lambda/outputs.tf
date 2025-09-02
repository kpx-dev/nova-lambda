output "fastapi_function_arn" {
  description = "FastAPI Lambda Function ARN (streaming)"
  value       = aws_lambda_function.fastapi_function.arn
}

output "fastapi_function_name" {
  description = "FastAPI Lambda Function Name (streaming)"
  value       = aws_lambda_function.fastapi_function.function_name
}

output "lambda_role_arn" {
  description = "IAM role ARN for the Lambda function"
  value       = aws_iam_role.lambda_role.arn
}

output "function_names" {
  description = "Lambda function names for CLI invocation"
  value = {
    streaming = aws_lambda_function.fastapi_function.function_name
  }
}

output "ecr_image_uri" {
  description = "ECR image URI used by Lambda functions"
  value       = local.image_uri
}

output "ecr_repository_url" {
  description = "ECR repository URL for pushing images"
  value       = aws_ecr_repository.fastapi_repo.repository_url
}

output "docker_build_commands" {
  description = "Commands to build and push Docker image"
  value = [
    "# Build the Docker image",
    "docker build -t ${var.ecr_repository_name} ./app",
    "",
    "# Get ECR login token",
    "aws ecr get-login-password --region ${var.aws_region} | docker login --username AWS --password-stdin ${aws_ecr_repository.fastapi_repo.repository_url}",
    "",
    "# Tag and push the image",
    "docker tag ${var.ecr_repository_name}:latest ${aws_ecr_repository.fastapi_repo.repository_url}:${var.image_tag}",
    "docker push ${aws_ecr_repository.fastapi_repo.repository_url}:${var.image_tag}"
  ]
}