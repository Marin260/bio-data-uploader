from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import require_admin
from persistence.repository import UserQueries, user_repo

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_admin)])

# TODO: admin routes (manage users and files)


@router.post("/users/block/{user_id}")
def block_user(user_id: int, db: UserQueries = Depends(user_repo)):
    blocked_user = db.block_user(user_id)
    if block_user is None:
        raise HTTPException(status_code=404, detail="Requested User Not Found")
    return block_user


@router.post("/users/unblock/{user_id}")
def unblock_user(user_id: int, db: UserQueries = Depends(user_repo)):
    unblocked_user = db.unblock_user(user_id)
    if unblock_user is None:
        raise HTTPException(status_code=404, detail="Requested User Not Found")
    return unblocked_user


@router.delete("/users/delete/{user_id}", status_code=204)
def delete_user(user_id: int, db: UserQueries = Depends(user_repo)):
    db.delete_user(user_id)
    return


# TODO: manage minio files routes
