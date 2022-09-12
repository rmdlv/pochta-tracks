import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_PARSER = os.environ.get("DEFAULT_PARSER")
USER_AGENT = os.environ.get("USER_AGENT")
