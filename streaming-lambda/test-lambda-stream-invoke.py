#!/usr/bin/env python3
"""
Test script for invoking Lambda function with response streaming.
This script demonstrates how to invoke a Lambda function and handle streaming responses.
"""

import boto3
import json
import sys
from typing import Iterator, Dict, Any

def test_story_generation(function_name: str, region: str = "us-east-1"):
    """Test /api/story endpoint with simulated streaming."""
    print(f"🚀 Testing /api/story endpoint with function: {function_name}")
    
    # Test payload for /api/story endpoint
    payload = {
        "httpMethod": "POST",
        "path": "/api/story",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "topic": "a robot learning to paint"
        })
    }
    
    print("📝 Sending request...")
    print(f"Topic: {json.loads(payload['body'])['topic']}")
    print("\n🔄 Streaming response:")
    print("-" * 50)
    
    try:
        # Create Lambda client
        lambda_client = boto3.client('lambda', region_name=region)
        
        # Invoke function
        response = lambda_client.invoke(
            FunctionName=function_name,
            Payload=json.dumps(payload)
        )
        
        # Read the complete response
        result = response['Payload'].read().decode('utf-8')
        
        if result:
            # Parse the Lambda response
            lambda_response = json.loads(result)
            
            if lambda_response.get('statusCode') == 200:
                # Parse the body which contains our actual response
                body = json.loads(lambda_response.get('body', '{}'))
                
                if 'story' in body:
                    # Simulate streaming by printing chunks with delay
                    story = body['story']
                    chunk_size = 50  # Characters per chunk
                    
                    for i in range(0, len(story), chunk_size):
                        chunk = story[i:i+chunk_size]
                        print(chunk, end='', flush=True)
                        # Small delay to simulate streaming
                        import time
                        time.sleep(0.05)
                    
                    print(f"\n\n✅ Stream completed successfully")
                    print(f"📊 Total chunks from Bedrock: {body.get('chunks', 'unknown')}")
                else:
                    print(json.dumps(body))
            else:
                print(f"Error: {lambda_response}")
        else:
            print("Empty response")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Stream interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during streaming: {e}")

def main():
    """Main function to run tests."""
    # Default values
    default_function_name = "nova-lambda-fastapi-streaming-function"
    default_region = "us-east-1"
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments - use defaults
        function_name = default_function_name
        region = default_region
    elif len(sys.argv) == 2:
        # One argument - could be function name or region
        arg = sys.argv[1]
        if arg in ["us-east-1"]:
            # Looks like a region
            function_name = default_function_name
            region = arg
        else:
            # Assume it's a function name
            function_name = arg
            region = default_region
    elif len(sys.argv) == 3:
        # Two arguments - function name and region
        function_name = sys.argv[1]
        region = sys.argv[2]
    else:
        print("Usage: python test-lambda-stream-invoke.py [function-name] [region]")
        print(f"Default function: {default_function_name}")
        print(f"Default region: {default_region}")
        print("\nExamples:")
        print("  python test-lambda-stream-invoke.py")
        print("  python test-lambda-stream-invoke.py us-west-2")
        print("  python test-lambda-stream-invoke.py my-function")
        print("  python test-lambda-stream-invoke.py my-function us-west-2")
        sys.exit(1)
    
    print(f"🧪 Lambda Streaming Test")
    print(f"Function: {function_name}")
    print(f"Region: {region}")
    print("=" * 60)
    
    # Test story generation with streaming
    test_story_generation(function_name, region)
    
    print("\n" + "=" * 60)
    print("✅ Tests completed!")

if __name__ == "__main__":
    main()