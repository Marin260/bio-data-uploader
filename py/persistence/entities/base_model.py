from peewee import Model

from ..db_connection import database


class BaseModel(Model):
    class Meta:
        database = database
