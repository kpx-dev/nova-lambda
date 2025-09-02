import json
import boto3
from botocore.config import Config

boto_config = Config(
    read_timeout=300,
    connect_timeout=10,
    retries={'max_attempts': 2}
)

def lambda_handler_non_stream(event, context):
    try:
        # Extract question from event
        question = event.get('question', 'What is the weather today?')
        model_id = event.get('model_id', 'us.amazon.nova-premier-v1:0')
        
        # Create Bedrock client using Lambda's execution role
        client = boto3.client(
            "bedrock-runtime", 
            region_name="us-east-1",
            config=boto_config
        )
        
        conversation = [
            {
                "role": "user",
                "content": [{"text": question}],
            }
        ]
        
        toolConfiguration = {
            "tools": [
                {
                    "systemTool": {
                        "name": "web_search_v1"
                    }
                }
            ]
        }
        
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            toolConfig=toolConfiguration,
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'question': question,
                'response': response['output']['message'],
                'requestId': response['ResponseMetadata']['RequestId']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def lambda_handler_stream(event, context):
    """
    Example using AWS Bedrock Converse Stream API for real-time responses
    """
    try:
        # Extract question from event
        question = event.get('question', 'What is the weather today?')
        model_id = event.get('model_id', 'us.amazon.nova-premier-v1:0')
        
        # Create Bedrock client using Lambda's execution role
        client = boto3.client(
            "bedrock-runtime", 
            region_name="us-east-1",
            config=boto_config
        )
        
        conversation = [
            {
                "role": "user",
                "content": [{"text": question}],
            }
        ]
        
        toolConfiguration = {
            "tools": [
                {
                    "systemTool": {
                        "name": "web_search_v1"
                    }
                }
            ]
        }
        
        # Use converse_stream for streaming responses
        response = client.converse_stream(
            modelId=model_id,
            messages=conversation,
            toolConfig=toolConfiguration,
        )
        
        # Collect streaming response
        full_response = ""
        tool_use_blocks = []
        
        for chunk in response['stream']:
            if 'messageStart' in chunk:
                # Message started
                continue
            elif 'contentBlockStart' in chunk:
                # Content block started
                continue
            elif 'contentBlockDelta' in chunk:
                # Streaming text content
                if 'text' in chunk['contentBlockDelta']['delta']:
                    text_chunk = chunk['contentBlockDelta']['delta']['text']
                    full_response += text_chunk
            elif 'contentBlockStop' in chunk:
                # Content block finished
                continue
            elif 'messageStop' in chunk:
                # Message finished
                break
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'question': question,
                'response': full_response,
                'streaming': True,
                'requestId': response['ResponseMetadata']['RequestId']
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e),
                'streaming': True
            })
        }