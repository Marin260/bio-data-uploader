from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import require_bearer
from api.models.requests import UserCreateRequest
from persistence.repository import UserQueries, user_repo

router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(require_bearer)])


@router.get("/users")
def get_users(user_queries: UserQueries = Depends(user_repo)):
    return user_queries.select_all_users()


@router.get("/users/{user_id}")
def get_user_by_id(user_id: int, user_queries: UserQueries = Depends(user_repo)):
    user = user_queries.select_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users/{user_email}")
def get_user_by_emial(user_email: str, user_queries: UserQueries = Depends(user_repo)):
    user = user_queries.select_user_by_email(user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users")
def create_user(request_user: UserCreateRequest, UserQueries=Depends(user_repo)):
    return user_repo.insert_user(request_user)
