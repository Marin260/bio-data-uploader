from typing import List

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from persistence.db_connection import get_db
from persistence.entities import User


class UserQueries:
    def __init__(self, db: Session):
        self.__db_session = db

    def select_all_users(self) -> List[User]:
        return self.__db_session.query(User).all()

    def select_user_by_id(self, user_id: int) -> User | None:
        return self.__db_session.query(User).filter_by(user_id=user_id).first()

    def select_user_by_email(self, email: str) -> User | None:
        user = self.__db_session.query(User).filter_by(email=email).first()
        return user

    def insert_user(self, user_email: str, status: bool = False) -> User:
        # TODO: should check and not rely on db exceptions
        try:
            user = User(email=user_email, blocked=status)
            self.__db_session.add(user)
            self.__db_session.commit()
            return user
        except IntegrityError:
            self.__db_session.rollback()

            existing_user = self.select_user_by_email(user_email)
            assert existing_user is not None

            return existing_user

    def block_user(self, user_id: int) -> User | None:
        user = self.select_user_by_id(user_id)

        if user is not None:
            user.blocked = True
            self.__db_session.commit()
            return user
        return None

    def unblock_user(self, user_id: int) -> User | None:
        user = self.select_user_by_id(user_id)

        if user is not None:
            user.blocked = False
            self.__db_session.commit()
            return user
        return None

    def delete_user(self, user_id: int) -> None:
        user = self.select_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Requested User Not Found")

        self.__db_session.delete(user)
        self.__db_session.commit()


def user_repo() -> UserQueries:
    db_session = get_db()
    return UserQueries(next(db_session))
