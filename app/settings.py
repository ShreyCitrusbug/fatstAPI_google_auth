import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG")


class Settings(BaseSettings):
    """
    Application settings
    """
    # Debug Settings
    DEBUG: bool = DEBUG

    # FastAPI Settings
    APP_NAME: str
    APP_VERSION: str

    # Google Auth Settings
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URL: str
    GOOGLE_ACCESS_TOKEN_URL: str
    GOOGLE_AUTHORIZE_URL: str
    GOOGLE_API_BASE_URL: str
    GOOGLE_JWKS_URI: str

    # CORS Settings
    ALLOWED_ORIGINS: str
    ALLOWED_HEADERS: str
    ALLOWED_METHODS: str

    # Logging Settings
    LOG_LEVEL: str

    # Frontend settings
    FRONTEND_URL: str

    @property
    def get_allowed_origin_settings(self) -> dict:
        """
        Function to return allowed origins, headers, and methods.

        ## Returns:
            `dict`: A dictionary containing the allowed origins, headers, and methods.
                - `allowed_origins`: A list of allowed origins.
                - `allowed_headers`: A list of allowed headers.
                - `allowed_methods`: A list of allowed methods.
        """
        return {
            "allowed_origins": self.ALLOWED_ORIGINS.split(","),
            "allowed_headers": self.ALLOWED_HEADERS.split(","),
            "allowed_methods": self.ALLOWED_METHODS.split(","),
        }

    @property
    def get_database_settings(self) -> dict:
        """
        Function to return database settings.

        ## Returns:
            `dict`: A dictionary containing the database settings.
                - `database`: The name of the database.
                - `user`: The username for the database.
                - `password`: The password for the database.
                - `host`: The host of the database.
                - `port`: The port of the database.
        """
        return {
            "database": self.DATABASE_NAME,
            "user": self.DATABASE_USER,
            "password": self.DATABASE_PASSWORD,
            "host": self.DATABASE_HOST,
            "port": self.DATABASE_PORT,
        }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
