from typing import List

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class User(Base):
    __tablename__ = "User"
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    blocked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    files: Mapped[List["File"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.user_id!r}, email={self.email!r})"
