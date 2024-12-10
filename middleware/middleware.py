import os
from datetime import datetime
from fastapi import Request
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the logging directory from environment variables
log_dir = os.getenv("LOG_DIR", "./logs")  # Default to ./logs if LOG_DIR is not set
os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists

# Define log file paths
request_log_file = os.path.join(log_dir, "request_log.txt")
response_log_file = os.path.join(log_dir, "response_log.txt")

async def log_request_response(request: Request, call_next):
    # Log request details
    with open(request_log_file, "a") as req_file:
        req_file.write(
            f"[{datetime.now()}] Request - Method: {request.method}, Path: {request.url.path}\n"
        )

    # Process the request and capture the response
    response = await call_next(request)

    # Log response details
    with open(response_log_file, "a") as res_file:
        res_file.write(
            f"[{datetime.now()}] Response - Status Code: {response.status_code}, Path: {request.url.path}\n"
        )

    return response