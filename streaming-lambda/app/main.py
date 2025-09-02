import boto3
import json
import os
import asyncio
from pydantic import BaseModel
from typing import Optional


class Story(BaseModel):
    topic: Optional[str] = None


bedrock = boto3.client('bedrock-runtime')


async def bedrock_stream(topic: str):
    instruction = f"""
    You are a world class writer. Please write a sweet bedtime story about {topic}.
    Make the story engaging, imaginative, and appropriate for children.
    """
    
    conversation = [
        {
            "role": "user",
            "content": [{"text": instruction}],
        }
    ]

    response = bedrock.converse_stream(
        modelId='us.amazon.nova-premier-v1:0',
        messages=conversation,
        inferenceConfig={
            "maxTokens": 1024,
            "temperature": 0.7
        }
    )

    stream = response.get('stream')
    if stream:
        for chunk in stream:
            if 'contentBlockDelta' in chunk:
                if 'text' in chunk['contentBlockDelta']['delta']:
                    text_chunk = chunk['contentBlockDelta']['delta']['text']
                    yield text_chunk
            elif 'messageStop' in chunk:
                yield "\n"
