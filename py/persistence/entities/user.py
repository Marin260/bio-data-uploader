from peewee import BooleanField, CharField, IntegerField

from .base_model import BaseModel


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    ad_id = CharField(unique=True, max_length=50)
    username = CharField(unique=True, max_length=50)
    email = CharField(unique=True, max_length=100)
    full_name = CharField(max_length=200)
    blocked = BooleanField(default=False)
