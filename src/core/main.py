from aiohttp import web

from src.conf.settings import DB_LOCATION, HOST, PORT
from src.core.startup_tasks import init_routes, init_db_session, create_db
import asyncio

from src.db.database import Database


def pre_init() -> None:
    """
    Pre-initialization that occurs before starting
    the server and connecting to the database.
    """
    create_db(DB_LOCATION)


def init(db_session: Database) -> web.Application:
    """
    Initializing the project, creating the necessary
    objects to start the server.

    :param db_session:
        The Database object to connect.
    """
    app = web.Application()

    init_routes(app)
    init_db_session(db_session)

    return app


async def run() -> None:
    """
    Initializing and starting the API server.
    """
    pre_init()

    async with Database(location=DB_LOCATION, handle_json_int_keys=True) as session:
        app = init(db_session=session)

        await web._run_app(
            app=app,
            host=HOST,
            port=PORT
        )

    return None


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
