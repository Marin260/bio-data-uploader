from faker import Faker

from persistence.db_connection import SessionLocal
from persistence.entities import User


def seed_user_table():
    fake = Faker()
    with SessionLocal() as session:
        for _ in range(50):
            fake_user = User(email=fake.email(), blocked=fake.boolean())
            session.add(fake_user)
        session.commit()
