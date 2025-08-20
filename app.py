import json
import boto3
from botocore.config import Config

boto_config = Config(
    read_timeout=300,
    connect_timeout=10,
    retries={'max_attempts': 2}
)

def lambda_handler(event, context):
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