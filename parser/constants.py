import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_PARSER = os.environ.get("DEFAULT_PARSER")
USER_AGENT = os.environ.get("USER_AGENT")

DB_CREDENTIALS = {
    "host": os.environ.get("POSTGRES_HOST"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "user": os.environ.get("POSTGRES_USER"),
    "port": os.environ.get("POSTGRES_PORT"),
    "database": os.environ.get("POSTGRES_DATABASE"),
}
