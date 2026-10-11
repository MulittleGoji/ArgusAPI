from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
import app.config as config

api_key = config.Settings()
header_scheme = APIKeyHeader(name = 'api_key')

def verify_api_key(key: str = Depends(header_scheme)):
    if key == api_key.api_key:
        return 'authenticated'
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")