import json
import asyncio
from main import bedrock_stream

def handler(event, context):
    """
    Lambda handler for direct invocation with response streaming
    """
    try:
        print(f"Received event: {json.dumps(event)}")
        
        # Handle HTTP-style events from test script
        if 'httpMethod' in event:
            method = event.get('httpMethod')
            path = event.get('path')
            
            if method == 'GET' and path == '/health':
                # For health check, return simple response
                response = {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'status': 'healthy', 'service': 'fastapi-lambda-streaming'})
                }
                print(f"Health check response: {response}")
                return response
            
            elif method == 'POST' and path == '/api/story':
                body = json.loads(event.get('body', '{}'))
                topic = body.get('topic', body.get('prompt', 'a magical adventure'))
                return handle_story_response(topic, context)
        
        # Handle direct invocation with topic
        else:
            topic = event.get('topic', 'a magical adventure')
            return handle_story_response(topic, context)
            
    except Exception as e:
        print(f"Error in handler: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def handle_story_response(topic: str, context):
    """Handle story generation with proper response"""
    try:
        print(f"Starting story response for topic: {topic}")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        story_chunks = []
        async def collect_story():
            print("Starting bedrock stream...")
            async for chunk in bedrock_stream(topic):
                print(f"Received chunk: {chunk[:50]}...")
                story_chunks.append(chunk)
        
        loop.run_until_complete(collect_story())
        loop.close()
        
        full_story = ''.join(story_chunks)
        print(f"Collected {len(story_chunks)} chunks, total length: {len(full_story)}")
        
        response = {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'topic': topic,
                'story': full_story,
                'mode': 'streaming',
                'chunks': len(story_chunks)
            })
        }
        
        print(f"Returning response with story length: {len(full_story)}")
        return response
        
    except Exception as e:
        print(f"Error in story response: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e), 'mode': 'streaming'})
        }
