# AWS Lambda Python with Bedrock Examples

This repository contains two examples demonstrating how to create AWS Lambda functions in Python that integrate with Amazon Bedrock.

## Examples

### 1. Streaming Response (`streaming-lambda/`)

A FastAPI-based Lambda function that demonstrates **streaming responses** from Bedrock models via direct invocation. This example shows how to:

- Stream real-time responses from Bedrock using direct Lambda invocation
- Use FastAPI with Lambda Web Adapter for containerized deployment
- Secure deployment without public function URLs
- Deploy using Docker containers with ARM64 architecture
- Test streaming responses using the included Python test script
- Handle both HTTP-style and direct invocation events

**Key Features:**

- ✅ No function URLs (enhanced security)
- ✅ Direct Lambda invocation with streaming support
- ✅ Comprehensive test script included
- ✅ Docker containerization
- ✅ Bedrock Nova model integration

### 2. Non-Streaming Response (`non-streaming-lambda/`)

A simple Lambda function that demonstrates **standard (non-streaming) responses** from Bedrock models. This example shows how to:

- Make synchronous calls to Bedrock
- Return complete responses at once
- Use traditional Lambda deployment patterns

## Quick Start

1. **Choose your approach:**

   - For streaming responses: `cd streaming-lambda`
   - For simple responses: `cd non-streaming-lambda`

2. **Deploy:**

   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Test streaming (streaming-lambda only):**
   ```bash
   python test-lambda-stream-invoke.py
   ```

## Security

Both examples follow AWS security best practices:

- IAM-based access control
- Least privilege permissions
- No public endpoints (function URLs disabled)
- ECR image scanning enabled
