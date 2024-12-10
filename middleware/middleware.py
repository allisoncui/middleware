import logging
from datetime import datetime
from fastapi import Request

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("./logs/microservice.log"),  # Logs to a file
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
