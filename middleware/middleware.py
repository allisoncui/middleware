import os
import jwt  # Import PyJWT library
from datetime import datetime
from fastapi import Request, HTTPException
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the logging directory and JWT Secret from environment variables
log_dir = os.getenv("LOG_DIR", "./logs")
JWT_SECRET = os.getenv("JWT_SECRET", "3b5d7c1a9b84f24baed6f0f6b3a72d12e4c5b3a9d6c2e8f1e7c3b4a3f5d8b9c")
JWT_ALGORITHM = "HS256"

os.makedirs(log_dir, exist_ok=True)

request_log_file = os.path.join(log_dir, "request_log.txt")
response_log_file = os.path.join(log_dir, "response_log.txt")

# JWT Validation Function
def validate_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload 
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Middleware to log requests, validate JWT, and log responses
async def log_request_response(request: Request, call_next):
    # JWT token validation
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    try:
        jwt_token = token.split(" ")[1]             # Extract the token part after 'Bearer'
        decoded_payload = validate_jwt(jwt_token)   # Validate the token
        request.state.user = decoded_payload        # Attach decoded user data to the request state
    except HTTPException as e:
        with open(request_log_file, "a") as req_file:
            req_file.write(
                f"[{datetime.now()}] Unauthorized Request - Method: {request.method}, Path: {request.url.path}, Error: {e.detail}\n"
            )
        raise

    # Log request details
    with open(request_log_file, "a") as req_file:
        req_file.write(
            f"[{datetime.now()}] Request - Method: {request.method}, Path: {request.url.path}, User: {request.state.user}\n"
        )

    response = await call_next(request)

    with open(response_log_file, "a") as res_file:
        res_file.write(
            f"[{datetime.now()}] Response - Status Code: {response.status_code}, Path: {request.url.path}\n"
        )

    return response


# import os
# from datetime import datetime
# from fastapi import Request
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# # Get the logging directory from environment variables
# log_dir = os.getenv("LOG_DIR", "./logs")  # Default to ./logs if LOG_DIR is not set
# os.makedirs(log_dir, exist_ok=True)  # Ensure the directory exists

# # Define log file paths
# request_log_file = os.path.join(log_dir, "request_log.txt")
# response_log_file = os.path.join(log_dir, "response_log.txt")

# async def log_request_response(request: Request, call_next):
#     # Log request details
#     with open(request_log_file, "a") as req_file:
#         req_file.write(
#             f"[{datetime.now()}] Request - Method: {request.method}, Path: {request.url.path}\n"
#         )

#     # Process the request and capture the response
#     response = await call_next(request)

#     # Log response details
#     with open(response_log_file, "a") as res_file:
#         res_file.write(
#             f"[{datetime.now()}] Response - Status Code: {response.status_code}, Path: {request.url.path}\n"
#         )

#     return response