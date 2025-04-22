from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.services import AuthorizationService

__security = HTTPBearer(bearerFormat="JWT")

# TODO: make this a bit nicer


def require_bearer(credentials: HTTPAuthorizationCredentials = Depends(__security)) -> None:
    authz_service = AuthorizationService()

    auth_header = credentials.credentials
    token = auth_header.split(" ")
    if not auth_header or not auth_header.startswith("Bearer") or len(token) < 2:
        raise HTTPException(status_code=401, detail="Invalid or missing Bearer token")
    try:
        authz_service.verify_token(token[1])
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")
