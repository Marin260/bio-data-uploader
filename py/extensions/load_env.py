import os

from dotenv import load_dotenv

# load the env file


def load_env() -> None:
    ENVIRONMENT = os.getenv("FLY_DAMS_ENVIRONMENT")

    if os.getenv("FLY_DAMS_ENVIRONMENT"):
        load_dotenv(f"settings/{ENVIRONMENT}/.env")
    else:
        load_dotenv(f"settings/.env")
