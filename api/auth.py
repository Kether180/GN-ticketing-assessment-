from fastapi import Header, HTTPException

API_KEY = "secret"  # Use it in production , use env var


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API KEY")
