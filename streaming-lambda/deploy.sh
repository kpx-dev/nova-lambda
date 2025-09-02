#!/bin/bash

set -e

# Configuration
AWS_REGION="us-east-1"
ECR_REPOSITORY="nova-lambda"
IMAGE_TAG="latest"

# Get AWS Account ID from current session
print_info() {
    echo -e "${YELLOW:-}$1${NC:-}"
}

print_info "Getting AWS Account ID from current session..."
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ] || [ -z "$AWS_ACCOUNT_ID" ]; then
    echo -e "${RED:-}✗ Failed to get AWS Account ID. Please ensure AWS CLI is configured.${NC:-}"
    exit 1
fi

print_info "Using AWS Account ID: ${AWS_ACCOUNT_ID}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}\n"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print info messages
print_info() {
    echo -e "${YELLOW}$1${NC}"
}

print_section "🚀 Starting FastAPI Lambda Deployment"

# Check if we're in the right directory
if [ ! -f "app/Dockerfile" ]; then
    print_error "Dockerfile not found. Please run this script from the streaming-lambda directory."
    exit 1
fi

if [ ! -f "main.tf" ]; then
    print_error "main.tf not found. Please run this script from the streaming-lambda directory."
    exit 1
fi

# Get ECR repository URL
ECR_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}"

print_section "📦 Step 1: Building and Pushing Docker Image"

print_info "Logging into ECR..."
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL}

if [ $? -eq 0 ]; then
    print_success "Successfully logged into ECR"
else
    print_error "Failed to login to ECR"
    exit 1
fi

print_info "Building Docker image for ARM64..."
docker build --platform linux/arm64 --provenance=false --sbom=false -f ./app/Dockerfile -t ${ECR_REPOSITORY}:${IMAGE_TAG} .

if [ $? -eq 0 ]; then
    print_success "Successfully built Docker image"
else
    print_error "Failed to build Docker image"
    exit 1
fi

print_info "Tagging image for ECR..."
docker tag ${ECR_REPOSITORY}:${IMAGE_TAG} ${ECR_URL}:${IMAGE_TAG}

print_info "Pushing image to ECR..."
docker push ${ECR_URL}:${IMAGE_TAG}

if [ $? -eq 0 ]; then
    print_success "Successfully pushed image to ECR"
    print_success "Image URI: ${ECR_URL}:${IMAGE_TAG}"
else
    print_error "Failed to push image to ECR"
    exit 1
fi

print_section "🏗️  Step 2: Deploying Infrastructure with Terraform"

print_info "Initializing Terraform..."
terraform init

if [ $? -eq 0 ]; then
    print_success "Terraform initialized successfully"
else
    print_error "Failed to initialize Terraform"
    exit 1
fi

print_info "Planning Terraform deployment..."
terraform plan

if [ $? -eq 0 ]; then
    print_success "Terraform plan completed successfully"
else
    print_error "Terraform plan failed"
    exit 1
fi

print_info "Applying Terraform configuration..."
terraform apply -auto-approve

if [ $? -eq 0 ]; then
    print_success "Terraform apply completed successfully"
else
    print_error "Terraform apply failed"
    exit 1
fi

print_section "🎉 Deployment Complete!"

# Get the function ARN from Terraform output
FUNCTION_ARN=$(terraform output -raw fastapi_function_arn 2>/dev/null || echo "Not available")
FUNCTION_NAME=$(terraform output -raw fastapi_function_name 2>/dev/null || echo "Not available")

echo -e "${GREEN}Your FastAPI Lambda function has been deployed successfully!${NC}\n"
echo -e "${YELLOW}Function ARN:${NC} ${FUNCTION_ARN}"
echo -e "${YELLOW}Function Name:${NC} ${FUNCTION_NAME}"
echo -e "${YELLOW}ECR Image:${NC} ${ECR_URL}:${IMAGE_TAG}"

echo -e "\n${BLUE}Test your deployment using the test script:${NC}"
echo -e "python test-lambda-stream-invoke.py ${FUNCTION_NAME} ${AWS_REGION}"

print_section "✅ Deployment Summary"
echo -e "• Docker image built and pushed to ECR"
echo -e "• Lambda function created/updated"
echo -e "• IAM roles and policies configured"
echo -e "• Bedrock access enabled"
echo -e "• Function URL disabled (use direct invoke for testing)"
echo ""
echo -e "${GREEN}Ready to handle streaming responses via direct invocation! 🚀${NC}"