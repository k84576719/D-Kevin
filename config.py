"""Application configuration loaded from environment variables.

Values fall back to sensible local-development defaults so the app can be run
without any extra setup, while still allowing full override in production via
environment variables (see .env.example).
"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "d_kevin")

    @classmethod
    def db_kwargs(cls):
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "database": cls.DB_NAME,
            "charset": "utf8mb4",
        }
