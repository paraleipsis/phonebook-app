import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env-example')

# The root directory of the project from which all paths will be formed.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

DB_NAME: str = os.environ.get("DB_NAME")
DB_LOCATION: Path = BASE_DIR / "db/data" / DB_NAME

HOST: str = os.environ.get("HOST")
PORT: int | str = os.environ.get("PORT")
SERVER_URL: str = f'http://{HOST}:{PORT}'
