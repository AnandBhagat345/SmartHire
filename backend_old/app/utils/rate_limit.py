import os
from fastapi import Request

def rate_limit_exempt(request: Request):
    return os.getenv("TESTING") == "true"