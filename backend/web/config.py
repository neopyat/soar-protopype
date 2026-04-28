from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATABASE_DIR / "soar.db"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_FILE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True