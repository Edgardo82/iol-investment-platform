import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "IOL Investment Platform"
    APP_VERSION: str = "0.1.0"

    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "iol_db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "iol_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "iol_password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://iol_user:iol_password@db:5432/iol_db"
    )


settings = Settings()
