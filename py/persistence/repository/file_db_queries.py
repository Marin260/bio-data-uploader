from typing import List

from sqlalchemy.orm import Session

from persistence.db_connection import get_db
from persistence.entities import File


class FileQueries:
    def __init__(self, db: Session):
        self.__db_session = db

    def select_all_files(self) -> List[File]:
        return self.__db_session.query(File).all()

    def select_file_by_id(self, file_id: int) -> File | None:
        return self.__db_session.query(File).filter_by(file_id=file_id).first()

    def select_file_by_storage_identifier(self, st_identifier: str) -> File | None:
        return self.__db_session.query(File).filter_by(file_storage_identifier=st_identifier).first()

    def select_file_by_file_name(self, file_name: str) -> File | None:
        return self.__db_session.query(File).filter_by(file_name=file_name).first()

    def insert_file(self, new_file: File) -> File:
        # TODO: should check and not rely on db exceptions
        try:
            file = File(
                file_name=new_file.file_name,
                file_storage_identifier=new_file.file_storage_identifier,
                file_size=new_file.file_size,
                user_id=new_file.user_id,
            )

            self.__db_session.add(file)
            self.__db_session.commit()
            return file
        except:
            self.__db_session.rollback()

            existing_file = self.select_file_by_name(new_file.file_name)
            assert existing_file is not None

            return existing_file


def file_repo() -> FileQueries:
    db_session = get_db()
    return FileQueries(next(db_session))
