import json
import os
from pathlib import Path

from aiohttp import web

from src.phonebook.router import setup_routes as setup_phonebook_routes
from src.phonebook.db_session import setup_session as setup_phonebook_session
from src.db.database import Database


def init_routes(application: web.Application) -> None:
    """
    Launching functions for initializing project applications routes.

    :param application:
        The aiohttp Application object to use in applications.
    """
    setup_phonebook_routes(application)


def init_db_session(session: Database) -> None:
    """
    Launching functions to transfer the initialized
    database session to the project applications.

    :param session:
        The Database session object to use in applications.
    """
    setup_phonebook_session(session)


def create_db(db_path: str | Path) -> None:
    """
    Creating a database (JSON file) if not exists.

    :param db_path:
        The path to JSON file.
    """

    if not os.path.exists(db_path):
        with open(db_path, 'w') as file:
            json.dump({}, file)
