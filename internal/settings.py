import os
import sys

IGNORE_CORS = bool(os.getenv("IGNORE_CORS", False))
LOG_JSON = bool(os.getenv("LOG_JSON", not sys.stderr.isatty()))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DB_URL = os.getenv("DB_URL", "sqlite://data/db.sqlite3")
