from .db_connection import database
from .entities.user import User


def create_tables():
    with database:
        database.create_tables([User])


create_tables()
