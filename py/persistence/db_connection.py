import os

from dotenv import load_dotenv
from playhouse.pool import PooledPostgresqlDatabase

ENVIRONMENT = os.getenv("FLY_DAMS_ENVIRONMENT")

# TODO: remove env loading once we start reading from secret manager

if os.getenv("FLY_DAMS_ENVIRONMENT"):
    load_dotenv(f"settings/{ENVIRONMENT}/.env")
else:
    load_dotenv(f"settings/.env")

database = PooledPostgresqlDatabase(
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    max_connections=10,
    stale_timeout=300,
)
