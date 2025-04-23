import os

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request

from api.services import AuthorizationService
from persistence.repository import UserQueries, user_repo

router = APIRouter(prefix="/auth", tags=["Auth"])

oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth_callback")

    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/callback")
async def auth_callback(request: Request, user_queries: UserQueries = Depends(user_repo)):
    authz_service = AuthorizationService()
    google_token = await oauth.google.authorize_access_token(request)

    user_email = google_token["userinfo"]["email"]

    if authz_service.google_id_token_is_valid(google_token):
        user = user_queries.select_user_by_email(user_email)
        if user is not None:
            pass
        else:
            user = user_queries.insert_user(user_email)

        access_token = authz_service.generate_access_token(user.email)
        return {"access_token": access_token}

    else:
        raise HTTPException(status_code=400, detail="Invalid login token")
