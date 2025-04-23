from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base


class File(Base):
    __tablename__ = "File"
    file_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(1000), nullable=False, unique=True)
    file_storage_identifier: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("User.user_id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="files")

    def __repr__(self) -> str:
        return f"File(identifier={self.file_storage_identifier}, name={self.file_name})"
