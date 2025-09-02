# FastAPI Lambda with Streaming Response

This example demonstrates how to create a Lambda function using FastAPI that streams responses from Amazon Bedrock models via direct invocation (without function URLs for enhanced security).

## Architecture

- **FastAPI**: Web framework for building the API
- **Lambda Web Adapter**: Enables FastAPI to run on Lambda
- **Amazon Bedrock**: AI service for generating streaming content
- **ECR**: Container registry for Docker images
- **Direct Invocation**: Secure method to invoke Lambda without public URLs

## Features

- ✅ Streaming responses from Bedrock Nova models
- ✅ FastAPI integration with Lambda
- ✅ Docker containerization with ARM64 support
- ✅ Direct Lambda invocation (no function URLs)
- ✅ Comprehensive IAM permissions for Bedrock
- ✅ Python test script for streaming validation
- ✅ Health check endpoint

## Project Structure

```
fastapi-response-streaming/
├── app/
│   ├── main.py              # FastAPI application
│   ├── lambda_handler.py    # Lambda handler for direct invocation
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Container configuration
│   └── static/             # Demo web interface
├── main.tf                 # Terraform infrastructure
├── variables.tf            # Terraform variables
├── outputs.tf              # Terraform outputs
├── deploy.sh               # Deployment script
├── test-lambda-stream-invoke.py  # Test script
└── README.md               # This file
```

## Prerequisites

- AWS CLI configured with appropriate permissions
- Docker installed and running
- Terraform installed
- Python 3.9+ for testing
- Access to Amazon Bedrock Nova models

## Deployment

1. **Configure variables** (optional):
   ```bash
   # Edit terraform.tfvars or use defaults
   cp terraform.tfvars.example terraform.tfvars
   ```

2. **Deploy everything**:
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

The deployment script will:
- Build and push Docker image to ECR
- Deploy Lambda function with Terraform
- Configure IAM roles and Bedrock permissions
- Output function name for testing

## Testing

### Using the Test Script

The included test script provides comprehensive testing of the streaming functionality:

```bash
# Test with function name from deployment output
python test-lambda-stream-invoke.py your-function-name us-east-1

# Example output:
# 🧪 Lambda Streaming Test
# Function: nova-lambda-fastapi-streaming-function
# Region: us-east-1
# ============================================================
# 
# 🏥 Testing health check with function: nova-lambda-fastapi-streaming-function
# Health check response: {"status":"healthy","service":"fastapi-lambda-streaming"}
# ✅ Stream completed successfully
# 
# 🚀 Testing story generation with function: nova-lambda-fastapi-streaming-function
# 📝 Sending request...
# Prompt: Write a short story about a robot learning to paint
# 
# 🔄 Streaming response:
# --------------------------------------------------
# Once upon a time, in a bustling workshop filled with gears and gadgets...
```

### Manual Testing with AWS CLI

```bash
# Health check
aws lambda invoke \
  --function-name your-function-name \
  --payload '{"httpMethod":"GET","path":"/health"}' \
  response.json && cat response.json

# Story generation
aws lambda invoke \
  --function-name your-function-name \
  --payload '{"httpMethod":"POST","path":"/generate-story","body":"{\"prompt\":\"a brave little mouse\"}"}' \
  response.json && cat response.json
```

## Configuration

### Environment Variables

The Lambda function uses these environment variables:
- `AWS_LWA_INVOKE_MODE`: Set to `RESPONSE_STREAM` for streaming support

### IAM Permissions

The function has permissions for:
- Bedrock model invocation (`bedrock:InvokeModelWithResponseStream`)
- CloudWatch logging
- X-Ray tracing

### Bedrock Models

Currently configured to use:
- `us.amazon.nova-premier-v1:0` (can be changed in `app/main.py`)

## Security Considerations

- **No Function URLs**: Direct invocation only for enhanced security
- **IAM-based access**: All access controlled through AWS IAM
- **Least privilege**: Minimal required permissions only
- **VPC support**: Can be deployed in VPC if needed (modify Terraform)

## Troubleshooting

### Common Issues

1. **Bedrock Access Denied**:
   - Ensure your AWS account has access to Bedrock models
   - Check IAM permissions in the Lambda role

2. **Docker Build Fails**:
   - Ensure Docker is running
   - Check ARM64 platform support

3. **ECR Push Fails**:
   - Verify AWS credentials and region
   - Check ECR repository permissions

4. **Lambda Timeout**:
   - Increase timeout in `main.tf` (currently 300 seconds)
   - Monitor CloudWatch logs for performance issues

### Logs and Monitoring

- **CloudWatch Logs**: `/aws/lambda/your-function-name`
- **X-Ray Tracing**: Enabled for performance monitoring
- **ECR Scanning**: Enabled for security vulnerability detection

## Customization

### Changing the Bedrock Model

Edit `app/main.py`:
```python
response = bedrock.converse_stream(
    modelId='us.amazon.nova-lite-v1:0',  # Change model here
    messages=conversation,
    # ...
)
```

### Adding New Endpoints

Add routes to `app/main.py` and update the handler in `app/lambda_handler.py`.

### Modifying Streaming Behavior

The streaming logic is in the `bedrock_stream` function in `app/main.py`.

## Cost Optimization

- Uses ARM64 architecture for better price/performance
- Configurable memory and timeout settings
- ECR lifecycle policies can be added for image cleanup

## Next Steps

- Add authentication/authorization
- Implement rate limiting
- Add monitoring and alerting
- Consider API Gateway integration for public APIs
- Add VPC configuration for enhanced security