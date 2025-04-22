from typing import Optional

from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    email: str
    blocked: Optional[bool] = False
