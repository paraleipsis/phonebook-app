from db.database import Database
from typing import Optional

_db_session: Optional[Database]


def setup_session(session: Database) -> Database:
    """
    Initialize new database session in current application (Phonebook).

    :param session:
        New database session.
    """
    global _db_session

    _db_session = session

    return _db_session


def get_session() -> Database:
    """
    Get active database session.
    """
    return _db_session
