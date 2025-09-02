import os
import subprocess
import sys
import time
import threading
from main import app

def start_server():
    """Start the FastAPI server in a separate thread"""
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

def handler(event, context):
    """Lambda handler that starts FastAPI server"""
    # Start the server in a background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Give the server a moment to start
    time.sleep(1)
    
    # The Lambda Web Adapter will handle the HTTP routing
    return {"statusCode": 200, "body": "Server started"}
