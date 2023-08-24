from functools import wraps
from asyncio.exceptions import CancelledError
from typing import Hashable

from logger.logs import logger
from os import listdir
from os.path import isfile, join, abspath

from typing_extensions import Any


def catch_exception(func: callable, *args, **kwargs) -> callable:
    """
    Catch base exception of callable and return None if it occurs.
    """
    try:
        return func(*args, **kwargs)
    except Exception as exc:
        logger['error'].info(f'Error: {repr(exc)}')
        return None


def graceful_shutdown(func: callable) -> callable:
    """
    Wrapper for graceful shutdown with saving storage
    data on disc if some Exception occurs.


    :param func:
        Entry point func that contains Database instance
    """
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            await func(self, *args, **kwargs)
        except (KeyboardInterrupt, CancelledError):
            await self.db.write()
            logger['info'].info('Shutdown ...')
        except Exception as exc:
            await self.db.write()
            logger['error'].info(f'Shutdown error: {repr(exc)}')

    return wrapper


def deep_update(mapping: dict[Hashable, Any], *updating_mappings: dict[Hashable, Any]) -> dict[Hashable, Any]:
    """
    Update all nested mappings of a given mapping.

    :param mapping:
        Mapping to update.
    :param updating_mappings:
        New mappings.
    :return:
        Updated mapping.
    """
    updated_mapping = mapping.copy()
    for updating_mapping in updating_mappings:
        for k, v in updating_mapping.items():
            if k in updated_mapping and isinstance(updated_mapping[k], dict) and isinstance(v, dict):
                updated_mapping[k] = deep_update(updated_mapping[k], v)
            else:
                updated_mapping[k] = v
    return updated_mapping


def deep_search_by_pair(mapping: dict, key_value_pair: tuple) -> bool:
    """
    Search for tuple that represents key-value pair in given nested mapping.

    :param mapping:
        The mapping in which to search.
    :param key_value_pair:
        Tuple that represents key-value pair to search.

    :return:
        True if key-value pair found, else False.
    """
    for key, value in mapping.items():
        if key == key_value_pair[0] and value == key_value_pair[1]:
            return True

        if isinstance(value, list):
            for element in value:
                item = deep_search_by_pair(element, key_value_pair)
                if item:
                    return item

        if isinstance(value, dict):
            if deep_search_by_pair(value, key_value_pair):
                return True

    return False


def deep_search_by_key(key: Hashable, mapping: dict) -> Any:
    if isinstance(mapping, dict):
        if key in mapping:
            return mapping[key]
        for k, v in mapping.items():
            item = deep_search_by_key(key, mapping[k])
            if item is not None:
                return item
    elif isinstance(mapping, list):
        for element in mapping:
            item = deep_search_by_key(key, element)
            if item is not None:
                return item
    return None


def deep_delete_by_key(key: Hashable, mapping: dict) -> bool | None:
    if isinstance(mapping, dict):
        if key in mapping:
            del mapping[key]
            return True
        for k, v in mapping.items():
            item = deep_delete_by_key(key, mapping[k])
            if item is not None:
                return item
    elif isinstance(mapping, list):
        for element in mapping:
            item = deep_delete_by_key(key, element)
            if item is not None:
                return item
    return None


def list_json_files(json_files_dir: str) -> dict:
    json_files = {f: abspath(join(json_files_dir, f)) for f in listdir(json_files_dir)
                  if isfile(join(json_files_dir, f)) and f.endswith(".json")}

    return json_files
