import functools

from aiohttp import web
from src.modules.exceptions.api_exceptions import InvalidPageNum

from src.modules.schemas import response_schemas as schemas
from src.logger.logs import logger
from src.phonebook.exceptions import NoSuchEntry


def manage_exceptions(func):
    """
    Global exceptions handler for API views.

    :param func:
        API view to handle.
    """

    @functools.wraps(func)
    async def wrap_func(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except NoSuchEntry as e:
            logger['error'].error(
                f'{type(e).__name__}: {str(e)}'
            )
            return web.json_response(
                status=404,
                data=schemas.GenericResponseModel(success=False, error_msg=str(e)).dict()
            )
        except Exception as e:
            logger['error'].error(
                f'{type(e).__name__}: {repr(e)}'
            )
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=str(e)).dict()
            )

        return result

    return wrap_func


def paginator(items, page_num: int = 1, page_size: int = 5) -> list:
    """
    Split list to a given number of lists with given size.

    :param items:
        List to split.
    :param page_num:
        Number of sublists.
    :param page_size:
        Amount of items in each sublist.
    """

    if len(items) < 1:
        return []

    if page_num < 1:
        raise InvalidPageNum("Page number must be > 0")

    page_num -= 1

    pages = [items[i:i+page_size] for i in range(0, len(items), page_size)]

    try:
        return pages[page_num]
    except IndexError:
        return pages[-1]
