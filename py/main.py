import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.routes import (
    admin_routes,
    auth_routes,
    file_routes,
    legacy_routes,
    user_routes,
)
from extensions import load_env

load_env.load_env()

app = FastAPI()

# TODO: ratelimit app

app.add_middleware(SessionMiddleware, secret_key=os.getenv("MIDDLEWARE_SESSION_SECRET"))

app.include_router(file_routes.router)
app.include_router(user_routes.router)
app.include_router(admin_routes.router)
app.include_router(auth_routes.router)
app.include_router(legacy_routes.router)


@app.get("/ping")
def healthCheck():
    return {"Hello": "World"}
