import logging
from datetime import datetime
from fastapi import Request
import os

log_dir = os.getenv("LOG_DIR", "./logs")
log_file = os.path.join(log_dir, "microservice.log")

os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Logs to a file
        logging.StreamHandler()  # Logs to the console
    ]
)

async def log_request_response(request: Request, call_next):
    # Log request details
    logging.info(f"Request - Method: {request.method}, Path: {request.url.path}, Time: {datetime.now()}")

    # Process the request and capture the response
    response = await call_next(request)

    # Log response details
    logging.info(f"Response - Status Code: {response.status_code}, Path: {request.url.path}, Time: {datetime.now()}")

    return response
