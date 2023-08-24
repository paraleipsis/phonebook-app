import json
from pathlib import Path
from types import TracebackType
from typing import Hashable, Any, List, Tuple, MutableMapping

import aiofiles

from io import UnsupportedOperation
from os.path import basename

from aiofiles.base import AiofilesContextManager
from db.exceptions import KeyAlreadyExist
from db.utils import catch_exception, deep_update, deep_search_by_pair
from typing_extensions import Optional, Type


class Connection:
    """
    Class for low-level interacting with JSON file descriptor.
    All arguments should be passed through connect factory method.
    """
    def __init__(self):
        self.connection: Optional[Path] = None
        self.read_only: Optional[bool] = None
        self.location: Optional[str] = None
        self.data: Optional[dict] = None
        self.encoding: Optional[str] = None

    @classmethod
    async def connect(
            cls,
            location: str | Path,
            read_only: bool = False,
            encoding: str = 'utf8',
            **kwargs
    ) -> "Connection":
        """
        Factory method to create a new connection to JSON file instance.

        :param location:
            Path to JSON file to open.
        :param read_only:
            Open JSON file only for reading.
        :param encoding:
            JSON file encoding.
        """
        self = cls()
        self.location = location
        self.encoding = encoding
        self.read_only = read_only
        self.connection = await self.open_db()
        self.data = await self.read(**kwargs)
        return self

    async def open_db(self) -> AiofilesContextManager:
        """
        Open JSON file descriptor.
        """
        if self.read_only:
            file = await aiofiles.open(self.location, encoding=self.encoding, mode='r')
        else:
            file = await aiofiles.open(self.location, encoding=self.encoding, mode='r+')

        return file

    async def disconnect(self):
        """
        Close JSON file.
        """
        if self.connection is not None:
            await self.connection.close()
            self.connection = None

    async def read(self, handle_json_int_keys: bool = False) -> dict:
        """
        Read all data from opened JSON file to memory.

        :param handle_json_int_keys:
            Convert all JSON keys to int.

        :return:
            Deserialized JSON data to dictionary.
        """
        file = await self.connection.read()

        if handle_json_int_keys:
            data = json.loads(
                file,
                object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()}
            )
        else:
            data = json.loads(file)

        return data

    async def write(self) -> bool:
        """
        Write new object to JSON file.
        Seek first position of file, add new object
        and truncate old object from file.
        """
        if self.read_only:
            raise UnsupportedOperation(f"{basename(self.location)} is not writable")

        await self.connection.seek(0)
        await self.connection.write(json.dumps(self.data))
        await self.connection.truncate()

        return True


class Database:
    """
    Class for interacting with key-value in-memory data storage based on JSON format.

    :param location:
        Path of JSON file to connect and use as database.
    :param read_only:
        Connect to JSON-based database only for reading data.
    :param handle_json_int_keys:
        After opening convert all keys of received object to int.
    """
    def __init__(
            self,
            location: str | Path,
            read_only: bool = False,
            handle_json_int_keys: bool = False
    ):
        self.read_only: Optional[bool] = read_only
        self.location: Optional[Path] = location
        self._db_session: Optional[Connection] = None
        self.handle_json_int_keys: Optional[bool] = handle_json_int_keys

    async def __aenter__(self) -> "Database":
        self._db_session = await Connection.connect(
            location=self.location,
            read_only=self.read_only,
            handle_json_int_keys=self.handle_json_int_keys
        )

        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ):
        await self._db_session.disconnect()

    def get(self, key: Hashable, default=None) -> Any | None:
        """
        Get value from key-value storage by its key.

        :param key:
            Key of value to get.
        :param default:
            Default value to return if key is not found in storage.

        :return:
            Objects by given key.
        """
        try:
            return self._db_session.data[key]
        except KeyError:
            return default

    def get_many(self, keys: list) -> list:
        """
        Get list of values by specific keys.
        If there is no such key then value will be None.

        :param keys:
            List of keys to get.

        :return:
            List of objects by given keys.
        """
        return [catch_exception(lambda: self._db_session.data[key]) for key in keys]

    def get_all(self) -> dict:
        """
        Get all data from storage.

        :return:
            All data from storage
        """
        return self._db_session.data

    def delete(self, key: Hashable) -> bool:
        """
        Delete value from storage.

        :param key:
            Key to delete.

        :return:
            True if success, False if key not found in storage.
        """
        try:
            del self._db_session.data[key]
        except KeyError:
            return False
        return True

    def add(self, new_data: Any, key: Hashable = None) -> bool:
        """
        Add new data to in-memory storage.
        After call this method does not save new data
        on disc and just update it in memory,
        for writing this you should use "save" method

        :param new_data:
            New value to add.
        :param key:
            Key for new value.
        """
        if self._db_session.data.get(key) is not None:
            raise KeyAlreadyExist(f"Key {key} already exist in {self.location}")

        self._db_session.data[key] = new_data
        return True

    def merge(self, new_data: MutableMapping) -> bool:
        """
        Merge new data object and storage object

        :param new_data:
            New object to merge.
        """
        self._db_session.data = self._db_session.data | new_data
        return True

    def update(self, key: Hashable, data: Any) -> bool:
        """
        Update data by given key. Using deep update so even nested objects can be updated.

        :param key:
            Key of object to update.
        :param data:
            Data to update.
        """
        self._db_session.data[key] = deep_update(self._db_session.data[key], data)
        return True

    async def save(self) -> bool:
        """
        Save new object in memory to disc. Works like commit.
        """
        await self._db_session.write()
        return True

    def search(self, search_query: List[Tuple]) -> List[Hashable]:
        """
        Storage search by provided key-value pairs.
        The root key will be returned if its object or nested
        objects satisfy the search query.

        :param search_query:
            List of tuples with key-value pair represents query to find.
        :return:
            List of found keys by search query.
        """
        results = []

        if len(search_query) == 0:
            return results

        if len(search_query) == 1:
            if self._db_session.data.get(search_query[0][0]) == search_query[0][1]:
                results.append(search_query[0][0])

        for key, value in self._db_session.data.items():
            if isinstance(value, dict):
                if all(deep_search_by_pair(key_value_pair=q, mapping=value) for q in search_query):
                    results.append(key)

        return results

    def __repr__(self):
        return f'{self.__class__.__name__}("{self._db_session.location}")'
