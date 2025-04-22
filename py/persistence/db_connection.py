import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENVIRONMENT = os.getenv("FLY_DAMS_ENVIRONMENT")

# TODO: remove env loading once we start reading from secret manager

if os.getenv("FLY_DAMS_ENVIRONMENT"):
    load_dotenv(f"settings/{ENVIRONMENT}/.env")
else:
    load_dotenv(f"settings/.env")

# dbUrl = f"sqlite+{os.getenv("TURSO_DATABASE_URL")}/?authToken={os.getenv("TURSO_AUTH_TOKEN")}&secure=true"
dbUrl = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}"

engine = create_engine(dbUrl, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    with SessionLocal() as session:
        yield session
