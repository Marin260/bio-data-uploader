from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.services import AuthorizationService

__security = HTTPBearer(bearerFormat="JWT")

# TODO: make this a bit nicer


def require_bearer(credentials: HTTPAuthorizationCredentials = Depends(__security)) -> None:
    authz_service = AuthorizationService()

    token = credentials.credentials
    if not token or credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid or missing Bearer token")
    try:
        authz_service.verify_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")
