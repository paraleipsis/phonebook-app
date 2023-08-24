from typing import List, Mapping

from src.db.exceptions import KeyAlreadyExist
from src.phonebook.db_session import get_session
from src.modules.utils.utils import convert_obj_to_list, filter_none_values
from src.modules.utils.api_utils import paginator
from src.phonebook.exceptions import NoSuchEntry
from src.phonebook.schemas.entry_schemas import EntryCreate
from src.phonebook.utils import generate_id


async def get_entry_list(page_num: int, page_size: int, **kwargs) -> List[Mapping]:
    db_session = get_session()
    query_params = list(filter_none_values(kwargs).items())

    if not query_params:
        data = convert_obj_to_list(db_session.get_all())
        paginate_data = paginator(data, page_num=page_num, page_size=page_size)
    else:
        data_keys = db_session.search(search_query=query_params)
        data = db_session.get_many(data_keys)
        paginate_data = paginator(data, page_num=page_num, page_size=page_size)

    return paginate_data


async def get_entry(entry_id: int) -> Mapping:
    db_session = get_session()
    data = db_session.get(key=entry_id)

    if not data:
        raise NoSuchEntry(f"Entry with ID {entry_id} does not exist")

    return data


async def delete_entry(entry_id: int) -> bool:
    db_session = get_session()
    data = db_session.delete(key=entry_id)

    if not data:
        raise NoSuchEntry(f"Entry with ID {entry_id} does not exist")

    await db_session.save()

    return data


async def create_entry(entry: EntryCreate) -> Mapping:
    db_session = get_session()

    entry_key = None
    while True:
        try:
            entry_key = generate_id(data=db_session.get_all())
            db_session.add(key=entry_key, new_data=entry.dict())
        except KeyAlreadyExist:
            continue
        else:
            break

    data = db_session.get(key=entry_key)

    await db_session.save()

    return data


async def update_entry(entry_id: int, entry: EntryCreate) -> Mapping:
    db_session = get_session()
    entry_d = db_session.get(key=entry_id)

    if not entry_d:
        raise NoSuchEntry(f"Entry with ID {entry_id} does not exist")

    db_session.update(key=entry_id, data=entry.dict())
    data = db_session.get(key=entry_id)

    await db_session.save()

    return data
