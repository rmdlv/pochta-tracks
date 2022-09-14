import os

from dotenv import load_dotenv

load_dotenv(".env")

DB_URL = os.environ.get("DB_URL")
