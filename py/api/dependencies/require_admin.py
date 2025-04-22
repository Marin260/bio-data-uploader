import os

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.services import AuthorizationService

__security = HTTPBearer(bearerFormat="JWT")

# TODO: make this a bit nicer


def require_admin(credentials: HTTPAuthorizationCredentials = Depends(__security)) -> None:
    authz_service = AuthorizationService()

    auth_header = credentials.credentials
    token = auth_header.split(" ")
    if not auth_header or not auth_header.startswith("Bearer") or len(token) < 2:
        raise HTTPException(status_code=401, detail="Invalid or missing Bearer token")
    try:
        if authz_service.verify_admin_token(token[1]) == False:
            # TODO: fix this, it will get caught by the next except
            raise HTTPException(status_code=403, detail="Permission Denied")

    except:
        raise HTTPException(status_code=401, detail="Invalid Token")
